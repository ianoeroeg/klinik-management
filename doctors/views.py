from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count, Avg, Max
from datetime import date, datetime, timedelta
from django.utils import timezone

from .models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Invoice


def doctor_dashboard_required(view_func):
    """Decorator pikeun ngan dokter anu bisa ngaksés dashboardna sorangan."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            doctor = Doctor.objects.select_related('user').get(user=request.user)
        except Doctor.DoesNotExist:
            messages.error(request, 'Profil dokter anjeun teu kapanggih.')
            return redirect('home')
        # Override kwargs to pass doctor instead of pk
        kwargs['doctor'] = doctor
        if 'pk' in kwargs:
            del kwargs['pk']
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@doctor_dashboard_required
def doctor_dashboard(request, doctor):
    """Doctor Dashboard - ringkesan padamelan dokter."""
    now = datetime.now()
    today = date.today()
    current_month = today.month
    current_year = today.year
    
    # Today's appointments
    today_appointments = Appointment.objects.select_related(
        'patient'
    ).filter(
        doctor=doctor,
        appointment_date=today
    ).order_by('appointment_time')
    
    # Total patients treated by this doctor
    total_patients = Appointment.objects.filter(
        doctor=doctor
    ).values('patient').distinct().count()
    
    # Patients this month
    patients_this_month = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__month=current_month,
        appointment_date__year=current_year
    ).values('patient').distinct().count()
    
    # Revenue today (from paid invoices for this doctor's appointments)
    today_revenue = Invoice.objects.filter(
        appointment__doctor=doctor,
        status='paid',
        created_at__date=today
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Monthly revenue
    monthly_revenue = Invoice.objects.filter(
        appointment__doctor=doctor,
        status='paid',
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Total prescriptions
    total_prescriptions = Prescription.objects.filter(
        appointment__doctor=doctor
    ).count()
    
    # Prescriptions today
    prescriptions_today = Prescription.objects.filter(
        appointment__doctor=doctor,
        created_at__date=today
    ).count()
    
    # Recent patients (last 10)
    recent_patients = Patient.objects.filter(
        appointments__doctor=doctor
    ).annotate(
        last_appointment=Max('appointments__appointment_date')
    ).order_by('-last_appointment')[:10]
    
    # Pending invoices (for this doctor's appointments)
    pending_invoices = Invoice.objects.filter(
        appointment__doctor=doctor,
        status__in=['pending', 'unpaid']
    ).order_by('-created_at')[:10]
    
    # Upcoming appointments (next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_appointments = Appointment.objects.select_related(
        'patient'
    ).filter(
        doctor=doctor,
        appointment_date__gte=today,
        appointment_date__lte=next_week
    ).order_by('appointment_date', 'appointment_time')
    
    # Revenue chart data (last 7 days)
    revenue_labels = []
    revenue_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_rev = Invoice.objects.filter(
            appointment__doctor=doctor,
            status='paid',
            created_at__date=day
        ).aggregate(total=Sum('total'))['total'] or 0
        revenue_labels.append(day.strftime('%d/%m'))
        revenue_data.append(int(day_rev))
    
    month_names = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'Séptémber', 'Oktober', 'Nopémber', 'Desémber'
    ]
    current_month_name = month_names[current_month - 1]
    
    context = {
        'doctor': doctor,
        'now': now,
        'today_appointments': today_appointments,
        'today_appointments_count': today_appointments.count(),
        'total_patients': total_patients,
        'patients_this_month': patients_this_month,
        'today_revenue': today_revenue,
        'monthly_revenue': monthly_revenue,
        'total_prescriptions': total_prescriptions,
        'prescriptions_today': prescriptions_today,
        'recent_patients': recent_patients,
        'pending_invoices': pending_invoices,
        'upcoming_appointments': upcoming_appointments,
        'revenue_labels': revenue_labels,
        'revenue_data': revenue_data,
        'current_month_name': current_month_name,
    }
    return render(request, 'doctors/doctor_dashboard.html', context)


@login_required
def doctor_list(request):
    doctors = Doctor.objects.select_related('user').all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})


@login_required
def doctor_detail(request, pk):
    doctor = Doctor.objects.select_related('user').get(pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})


@login_required
def doctor_toggle_availability(request, pk):
    """Toggle doctor availability."""
    if request.method == 'POST':
        doctor = Doctor.objects.get(pk=pk)
        doctor.is_available = not doctor.is_available
        doctor.save()
        messages.success(request, f'Status kasedia Dr. {doctor.user.get_full_name} dirobah.')
        return redirect('doctor_dashboard', pk=doctor.pk)
    return redirect('doctor_dashboard', pk=pk)
