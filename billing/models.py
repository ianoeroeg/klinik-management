from django.db import models
from django.conf import settings


class Invoice(models.Model):
    class Status(models.TextChoices):
        UNPAID = 'unpaid', 'Aya Tagihan'
        PAID = 'paid', 'Geus Dibayar'
        PARTIAL = 'partial', 'Bagean Dibayar'
        CANCELLED = 'cancelled', 'Dibatalkun'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Tunai'
        BANK_TRANSFER = 'bank_transfer', 'Transfer Bank'
        INSURANCE = 'insurance', 'Asuransi'
        E_WALLET = 'ewallet', 'E-Wallet'

    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.CASCADE,
        related_name='invoice',
        verbose_name='Appointment'
    )
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name='Pasien'
    )
    invoice_number = models.CharField(max_length=30, unique=True, verbose_name='No. Invoice')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Subtotal (Rp)')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Diskon (Rp)')
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Pajak (Rp)')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total (Rp)')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Jumlah Dibayar (Rp)')
    notes = models.TextField(blank=True, verbose_name='Catetan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_invoice'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoice-invoice'
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.patient}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            from datetime import datetime
            # Use a temporary ID if pk is None
            temp_id = self.pk if self.pk else 0
            self.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{temp_id:04d}"
        self.total = self.subtotal - self.discount + self.tax
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Invoice'
    )
    description = models.CharField(max_length=200, verbose_name='Katerangan')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Jumlah')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Harga Satuan (Rp)')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total (Rp)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'billing_invoice_item'
        verbose_name = 'Item Invoice'
        verbose_name_plural = 'Item-Item Invoice'
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} x{self.quantity}"


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = 'cash', 'Tunai'
        BANK_TRANSFER = 'bank_transfer', 'Transfer Bank'
        INSURANCE = 'insurance', 'Asuransi'
        E_WALLET = 'ewallet', 'E-Wallet'

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Invoice'
    )
    method = models.CharField(max_length=20, choices=Method.choices, verbose_name='Metode Pembayaran')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Jumlah (Rp)')
    payment_date = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=100, blank=True, verbose_name='No. Referensi')
    notes = models.TextField(blank=True, verbose_name='Catetan')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'billing_payment'
        verbose_name = 'Pembayaran'
        verbose_name_plural = 'Pembayaran-pembayaran'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Pembayaran {self.amount} - {self.invoice.invoice_number}"
