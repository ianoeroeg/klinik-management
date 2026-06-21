from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Patient
from appointments.models import Appointment
from billing.models import Invoice
from prescriptions.models import Prescription


def patient_portal_required(view_func):
    """Decorator pikeun ngan pasien anu bisa ngaksés portalna sorangan."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            patient = Patient.objects.get(user=request.user)
            # Check if user is trying to access their own portal
            if 'pk' in kwargs and kwargs['pk'] != patient.pk:
                messages.error(request, 'Anjeun teu bisa ngaksés data ieu.')
                return redirect('patient_portal')
        except Patient.DoesNotExist:
            messages.error(request, 'Profil pasien anjeun teu kapanggih.')
            return redirect('home')
        return view_func(request, patient=patient, *args, **kwargs)
    return wrapper


@login_required
def patient_portal(request, pk):
    """Patient Portal - pasien bisa ningali data sorangan waé."""
    from datetime import date
    
   # Get patient profile
    try:
        patient = Patient.objects.select_related('user').get(pk=pk)
    except Patient.DoesNotExist:
        messages.error(request, 'Profil pasien teu kapanggih.')
        return redirect('home')
    
    # Authorization check - patient can only access their own portal
    if request.user != patient.user:
        messages.error(request, 'Anjeun teu bisa ngaksés data ieu.')
        return redirect('home')
    
    from datetime import datetime
    now = datetime.now()
    
    # Get patient's appointments (upcoming)
    upcoming_appointments = Appointment.objects.select_related(
        'doctor'
    ).filter(
        patient=patient,
        appointment_date__gte=now
    ).order_by('appointment_date', 'appointment_time')
    
    # Get patient's invoices
    invoices = Invoice.objects.select_related(
        'appointment'
    ).filter(
        patient=patient
    ).order_by('-created_at')
    
     # Get patient's prescriptions
    prescriptions = Prescription.objects.filter(
        appointment__patient=patient
    ).prefetch_related('items__medicine', 'appointment__doctor').order_by('-created_at')
    
    context = {
        'patient': patient,
        'now': now,
        'upcoming_appointments': upcoming_appointments,
        'invoices': invoices,
        'prescriptions': prescriptions,
    }
    return render(request, 'patients/patient_portal.html', context)


@login_required
def patient_list(request):
    patients = Patient.objects.select_related('user').all()
    return render(request, 'patients/patient_list.html', {'patients': patients})


@login_required
def patient_detail(request, pk):
    patient = Patient.objects.select_related('user').get(pk=pk)
    return render(request, 'patients/patient_detail.html', {'patient': patient})


@login_required
def patient_create(request):
    if request.method == 'POST':
        # Simplified - in real app, use a form
        messages.info(request, 'Fitur tambah pasien - implementasi lengkap masih dalam pengembangan.')
        return redirect('patient_list')
    return render(request, 'patients/patient_form.html')


@login_required
def patient_update(request, pk):
    if request.method == 'POST':
        messages.info(request, 'Fitur edit pasien - implementasi lengkap masih dalam pengembangan.')
        return redirect('patient_list')
    return render(request, 'patients/patient_form.html')
