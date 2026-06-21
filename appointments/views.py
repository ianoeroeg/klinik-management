from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date

from .models import Appointment
from patients.models import Patient


@login_required
def appointment_list(request):
    today = date.today()
    queryset = Appointment.objects.select_related('patient', 'doctor').all()

    # Filter by date
    date_filter = request.GET.get('date')
    if date_filter:
        queryset = queryset.filter(appointment_date=date_filter)

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    # Filter by today
    today_filter = request.GET.get('today')
    if today_filter == '1':
        queryset = queryset.filter(appointment_date=today)

    return render(request, 'appointments/appointment_list.html', {
        'appointments': queryset,
        'today': today,
    })


@login_required
def appointment_detail(request, pk):
    appointment = Appointment.objects.select_related('patient', 'doctor').get(pk=pk)
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment,
    })


@login_required
def appointment_create(request):
    if request.method == 'POST':
        # Simplified - in real app, use a form with validation
        messages.info(request, 'Fitur tambah appointment - implementasi lengkap masih dalam pengembangan.')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_form.html')


@login_required
def appointment_update(request, pk):
    if request.method == 'POST':
        messages.info(request, 'Fitur edit appointment - implementasi lengkap masih dalam pengembangan.')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_form.html')


@login_required
def appointment_delete(request, pk):
    if request.method == 'POST':
        messages.info(request, 'Fitur hapus appointment - implementasi lengkap masih dalam pengembangan.')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html')


@login_required
def patient_portal_appointment_create(request):
    """Appointment create pikeun patient portal."""
    # Get patient from user
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, 'Profil pasien anjeun teu kapanggih.')
        return redirect('home')
    
    if request.method == 'POST':
        # Simplified - in real app, use a proper form with validation
        messages.info(request, 'Fitur tambah appointment - implementasi lengkap masih dalam pengembangan.')
        return redirect('patient_portal', pk=patient.pk)
    
    # Get available doctors
    from doctors.models import Doctor
    doctors = Doctor.objects.filter(is_available=True)
    
    context = {
        'patient': patient,
        'doctors': doctors,
    }
    return render(request, 'appointments/appointment_form.html', context)
