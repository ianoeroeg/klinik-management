from rest_framework import serializers
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from prescriptions.models import Medicine, Prescription, PrescriptionItem
from billing.models import Invoice, InvoiceItem, Payment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'phone', 'full_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name()


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'user_id', 'full_name', 'nik', 'date_of_birth', 'age', 'gender', 'blood_type',
                  'address', 'phone', 'emergency_contact', 'emergency_phone', 'created_at', 'updated_at']
        read_only_fields = ['id', 'age', 'created_at', 'updated_at', 'full_name']

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'user_id', 'full_name', 'license_number', 'specialization', 'education',
                  'experience_years', 'consultation_fee', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name']

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient', write_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), write_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_id', 'doctor', 'doctor_id', 'appointment_date', 'appointment_time',
                  'status', 'priority', 'reason', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'generic_name', 'form', 'manufacturer', 'unit', 'price', 'stock',
                  'expiry_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    medicine_id = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all(), source='medicine', write_only=True)

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medicine', 'medicine_id', 'dosage', 'frequency', 'duration', 'quantity']
        read_only_fields = ['id']


class PrescriptionSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all())
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'patient', 'diagnosis', 'treatment_notes', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'patient']

    def get_patient(self, obj):
        if obj and obj.appointment:
            return PatientSerializer(obj.appointment.patient).data
        return None


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'quantity', 'unit_price', 'total']
        read_only_fields = ['id', 'total']


class InvoiceSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
    payments = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    appointment_id = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all(), source='appointment', write_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'appointment_id', 'patient', 'status', 'subtotal', 'discount',
                  'tax', 'total', 'amount_paid', 'remaining', 'payment_method', 'notes', 'items', 'payments',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'invoice_number', 'created_at', 'updated_at', 'remaining', 'payments']

    def get_remaining(self, obj):
        return obj.total - obj.amount_paid

    def get_payments(self, obj):
        return PaymentSerializer(obj.payments.all(), many=True).data

    def create(self, validated_data):
        appointment = validated_data.get('appointment')
        if appointment:
            validated_data['patient'] = appointment.patient
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Include appointment as ID for read operations
        if instance.appointment:
            rep['appointment'] = instance.appointment.id
        else:
            rep['appointment'] = None
        return rep


class PaymentSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(read_only=True)
    invoice_id = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), source='invoice', write_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'invoice_id', 'method', 'amount', 'payment_date', 'reference_number']
        read_only_fields = ['id', 'payment_date']
