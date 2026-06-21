from django.db import models


class Prescription(models.Model):
    class Status(models.TextChoices):
        WRITTEN = 'written', 'Ditulisan'
        PAID = 'paid', 'Dibayar'
        DISPENSED = 'dispensed', 'Diresepkeun'
        CANCELLED = 'cancelled', 'Dibatalkun'

    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.CASCADE,
        related_name='prescription',
        verbose_name='Appointment'
    )
    diagnosis = models.TextField(verbose_name='Diagnosa')
    treatment_notes = models.TextField(blank=True, verbose_name='Catetan Pangobatan')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.WRITTEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prescriptions_prescription'
        verbose_name = 'Resep'
        verbose_name_plural = 'Resep-resep'
        ordering = ['-created_at']

    def __str__(self):
        return f"Resep - {self.appointment.patient} ({self.created_at.date()})"


class Medicine(models.Model):
    class Form(models.TextChoices):
        TABLET = 'tablet', 'Tablet'
        KAPLET = 'kaplet', 'Kaplet'
        SIRUP = 'sirup', 'Sirup'
        KREM = 'krim', 'Krim/Salep'
        INJEKSI = 'injeksi', 'Injeksi'
        KAPSUL = 'kapsul', 'Kapsul'
        TETES = 'tetes', 'Tetes'

    name = models.CharField(max_length=200, unique=True, verbose_name='Ngaran Obat')
    generic_name = models.CharField(max_length=200, blank=True, verbose_name='Ngaran Generik')
    form = models.CharField(max_length=20, choices=Form.choices, verbose_name='Bentuk')
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name='Produsen')
    unit = models.CharField(max_length=20, default='tablet', verbose_name='Satuan')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Harga (Rp)')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stok')
    expiry_date = models.DateField(blank=True, null=True, verbose_name='Batas Kadaluarsa')
    is_active = models.BooleanField(default=True, verbose_name='Aktip')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prescriptions_medicine'
        verbose_name = 'Obat'
        verbose_name_plural = 'Obat-obatan'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_form_display()}) - Stok: {self.stock}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Resep'
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT,
        related_name='prescription_items',
        verbose_name='Obat'
    )
    dosage = models.CharField(max_length=100, verbose_name='Dosis')
    frequency = models.CharField(max_length=100, verbose_name='Kadaliwuran')
    duration = models.CharField(max_length=100, verbose_name='Durasian')
    instructions = models.TextField(blank=True, verbose_name='Petunjuk')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Jumlah')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prescriptions_prescription_item'
        verbose_name = 'Item Resep'
        verbose_name_plural = 'Item-Item Resep'
        ordering = ['id']

    def __str__(self):
        return f"{self.medicine} - {self.dosage} ({self.frequency})"
