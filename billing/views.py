from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from datetime import date, timedelta

from .models import Invoice, InvoiceItem, Payment


@login_required
def invoice_list(request):
    invoices = Invoice.objects.select_related('patient').all()

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        invoices = invoices.filter(status=status_filter)

    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        invoices = invoices.filter(created_at__date__gte=date_from)
    if date_to:
        invoices = invoices.filter(created_at__date__lte=date_to)

    return render(request, 'billing/invoice_list.html', {
        'invoices': invoices,
    })


@login_required
def invoice_detail(request, pk):
    invoice = Invoice.objects.select_related('patient').prefetch_related('items', 'payments').get(pk=pk)
    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice,
    })


@login_required
def payment_create(request, invoice_pk):
    if request.method == 'POST':
        messages.info(request, 'Fitur tambah pembayaran - implementasi lengkap masih dalam pengembangan.')
        return redirect('invoice_detail', pk=invoice_pk)
    return render(request, 'billing/payment_form.html')


@login_required
def payment_list(request):
    payments = Payment.objects.select_related('invoice').all()
    return render(request, 'billing/payment_list.html', {'payments': payments})
