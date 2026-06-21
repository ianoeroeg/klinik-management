from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from datetime import date, timedelta

from appointments.models import Appointment
from billing.models import Invoice, Payment
from patients.models import Patient
from doctors.models import Doctor
from prescriptions.models import Medicine


@login_required
def dashboard(request):
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')

    # Stats
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.filter(is_available=True).count()
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    today_revenue = Invoice.objects.filter(
        created_at__date=today,
        status='paid'
    ).aggregate(total=Sum('total'))['total'] or 0

    # Recent appointments
    recent_appointments = Appointment.objects.select_related('patient', 'doctor').filter(
        appointment_date__gte=today
    ).order_by('appointment_date', 'appointment_time')[:10]

    # Recent invoices
    recent_invoices = Invoice.objects.select_related('patient').order_by('-created_at')[:10]

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'today_appointments': today_appointments,
        'today_revenue': today_revenue,
        'recent_appointments': recent_appointments,
        'recent_invoices': recent_invoices,
    }
    return render(request, 'reports/dashboard.html', context)
