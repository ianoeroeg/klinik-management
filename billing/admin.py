from django.contrib import admin
from .models import Invoice, InvoiceItem, Payment


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['payment_date']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'status', 'total', 'amount_paid', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['invoice_number', 'patient__user__first_name', 'patient__user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [InvoiceItemInline, PaymentInline]

    fieldsets = (
        ('Informasi Invoice', {'fields': ('invoice_number', 'appointment', 'patient', 'status')}),
        ('Perhitungan Harga', {'fields': ('subtotal', 'discount', 'tax', 'total', 'amount_paid')}),
        ('Pembayaran', {'fields': ('payment_method', 'notes')}),
        ('Timestamp', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'description', 'quantity', 'unit_price', 'total']
    list_filter = ['invoice__status']
    search_fields = ['description']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'method', 'amount', 'payment_date', 'reference_number']
    list_filter = ['method', 'payment_date']
    search_fields = ['invoice__invoice_number', 'reference_number']
    readonly_fields = ['payment_date']
