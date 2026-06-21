from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from prescriptions.models import Medicine, Prescription, PrescriptionItem
from billing.models import Invoice, InvoiceItem, Payment
from .serializers import (
    UserSerializer, PatientSerializer, DoctorSerializer, AppointmentSerializer,
    MedicineSerializer, PrescriptionSerializer, InvoiceSerializer, PaymentSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow admins to edit objects."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and (request.user.is_staff or request.user.is_superuser)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    filterset_fields = ['role', 'is_active']


class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for patients.
    """
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['user__first_name', 'user__last_name', 'nik', 'phone']
    filterset_fields = ['gender', 'blood_type']

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get patient statistics."""
        stats = {
            'total': self.queryset.count(),
            'male': self.queryset.filter(gender='L').count(),
            'female': self.queryset.filter(gender='P').count(),
        }
        return Response(stats)


class DoctorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for doctors.
    """
    queryset = Doctor.objects.select_related('user').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['user__first_name', 'user__last_name', 'license_number']
    filterset_fields = ['specialization', 'is_available']


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for appointments.
    """
    queryset = Appointment.objects.select_related('patient', 'doctor').all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['status', 'priority', 'appointment_date', 'doctor', 'patient']

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's appointments."""
        from django.utils import timezone
        today = timezone.now().date()
        appointments = self.queryset.filter(appointment_date=today)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update appointment status."""
        appointment = self.get_object()
        status_value = request.data.get('status')
        if status_value:
            appointment.status = status_value
            appointment.save()
            serializer = self.get_serializer(appointment)
            return Response(serializer.data)
        return Response({'error': 'Status required'}, status=status.HTTP_400_BAD_REQUEST)


class MedicineViewSet(viewsets.ModelViewSet):
    """
    API endpoint for medicines.
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['name', 'generic_name', 'manufacturer']
    filterset_fields = ['form', 'is_active']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get medicines with low stock."""
        low_stock = self.queryset.filter(stock__lte=10, is_active=True)
        serializer = self.get_serializer(low_stock, many=True)
        return Response(serializer.data)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for prescriptions.
    """
    queryset = Prescription.objects.select_related('appointment__patient').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['status', 'appointment__patient']


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for invoices.
    """
    queryset = Invoice.objects.select_related('patient').all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['invoice_number', 'patient__user__first_name']
    filterset_fields = ['status', 'payment_method']

    @action(detail=False, methods=['get'])
    def revenue(self, request):
        """Get revenue statistics."""
        from django.utils import timezone
        from django.db.models import Sum

        today = timezone.now().date()
        today_revenue = self.queryset.filter(
            status='paid', created_at__date=today
        ).aggregate(total=Sum('total'))['total'] or 0

        total_revenue = self.queryset.filter(status='paid').aggregate(total=Sum('total'))['total'] or 0

        return Response({
            'today': today_revenue,
            'total': total_revenue,
        })


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for payments.
    """
    queryset = Payment.objects.select_related('invoice').all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['method', 'invoice']

    def perform_create(self, serializer):
        """Override to handle payment logic."""
        invoice = serializer.validated_data['invoice']
        amount = serializer.validated_data['amount']

        # Check if payment amount is valid
        if amount > invoice.total - invoice.amount_paid:
            raise Exception('Payment amount exceeds remaining balance')

        # Create payment
        payment = serializer.save()

        # Update invoice amount paid
        invoice.amount_paid += amount
        invoice.save()

        # If fully paid, update status
        if invoice.amount_paid >= invoice.total:
            invoice.status = 'paid'
            invoice.save()
