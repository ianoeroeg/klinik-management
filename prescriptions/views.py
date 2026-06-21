from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Medicine, Prescription, PrescriptionItem


@login_required
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'prescriptions/medicine_list.html', {'medicines': medicines})


@login_required
def medicine_detail(request, pk):
    medicine = Medicine.objects.get(pk=pk)
    return render(request, 'prescriptions/medicine_detail.html', {'medicine': medicine})


@login_required
def prescription_list(request):
    prescriptions = Prescription.objects.select_related('appointment__patient').all()
    return render(request, 'prescriptions/prescription_list.html', {'prescriptions': prescriptions})


@login_required
def prescription_detail(request, pk):
    prescription = Prescription.objects.select_related('appointment__patient').prefetch_related('items__medicine').get(pk=pk)
    return render(request, 'prescriptions/prescription_detail.html', {'prescription': prescription})


@login_required
def prescription_create(request):
    if request.method == 'POST':
        messages.info(request, 'Fitur tambah resep - implementasi lengkap masih dalam pengembangan.')
        return redirect('prescription_list')
    return render(request, 'prescriptions/prescription_form.html')


@login_required
def prescription_update(request, pk):
    if request.method == 'POST':
        messages.info(request, 'Fitur edit resep - implementasi lengkap masih dalam pengembangan.')
        return redirect('prescription_list')
    return render(request, 'prescriptions/prescription_form.html')
