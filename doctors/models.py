from django.db import models
from django.conf import settings
from django.utils import timezone


class Doctor(models.Model):
    """Data dokter anu gawé di klinik."""

    class Specialization(models.TextChoices):
        UMUM = 'umum', 'Dokter Umum'
        GIGI = 'gigi', 'Dokter Gigi'
        KULIT = 'kulit', 'Dokter Kulit & Kelamin'
        ANAK = 'anak', 'Dokter Anak'
        JANTUNG = 'jantung', 'Dokter Jantung'
        THT = 'tnt', 'Dokter THT'
        MATA = 'mata', 'Dokter Mata'
        KANDUNGAN = 'kandungan', 'Dokter Kandungan'
        BEDAH = 'bedah', 'Dokter Bedah'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name='Pengguna'
    )
    license_number = models.CharField(max_length=50, unique=True, verbose_name='No. STR')
    specialization = models.CharField(
        max_length=20,
        choices=Specialization.choices,
        default=Specialization.UMUM,
        verbose_name='Spesialisasi'
    )
    education = models.CharField(max_length=200, blank=True, verbose_name='Pendidikan Terakhir')
    experience_years = models.PositiveIntegerField(default=0, verbose_name='Taun Pangalaman')
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Biaya Konsultasi (Rp)'
    )
    is_available = models.BooleanField(default=True, verbose_name='Sadayang Tersedia')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doctors_doctor'
        verbose_name = 'Dokter'
        verbose_name_plural = 'Dokter-dokter'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.get_specialization_display()})"

    @property
    def name(self):
        """Alias pikeun compatibility."""
        return self.user.get_full_name()
