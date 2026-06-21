from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    """Jadwal appointment pasien jeung dokter."""

    class Status(models.TextChoices):
        AJARAN = 'scheduled', 'Dijadwalkeun'
        DIBETAKEUN = 'in_progress', 'Dibérékeun'
        RÉNGSÉ = 'completed', 'Réngsé'
        DIBATALKEUN = 'cancelled', 'Dibatalkun'
        HADEUP = 'no_show', 'Henteu Teu (No Show)'

    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('emergency', 'Darurat'),
    ]

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Pasien'
    )
    doctor = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Dokter'
    )
    appointment_date = models.DateField(verbose_name='Tanggal Appointment')
    appointment_time = models.TimeField(verbose_name='Waktu Appointment')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AJARAN
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal'
    )
    reason = models.TextField(verbose_name='Alasan Kunjungan')
    notes = models.TextField(blank=True, verbose_name='Catetan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments_appointment'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointment-appointment'
        ordering = ['-appointment_date', '-appointment_time']
        indexes = [
            models.Index(fields=['doctor', 'appointment_date']),
            models.Index(fields=['patient', 'appointment_date']),
        ]

    def __str__(self):
        return f"{self.patient} - {self.doctor} ({self.appointment_date} {self.appointment_time})"

    def clean(self):
        """Validasi yén dokter teu aya appointment séjén dina waktos anu sarua."""
        if self.pk:
            existing = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
                appointment_time=self.appointment_time
            ).exclude(pk=self.pk)
        else:
            existing = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
                appointment_time=self.appointment_time
            )
        if existing.exists():
            raise ValidationError({
                'appointment_time': 'Dokter geus aya appointment séjén dina waktos ieu.'
            })
