from django.db import models
from django.conf import settings
from django.utils import timezone


class Patient(models.Model):
    """Data pasien anu datang ka klinik."""

    class Gender(models.TextChoices):
        LAKI = 'L', 'Laki-laki'
        PAWAWAI = 'P', 'Pawéwé'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        verbose_name='Pengguna'
    )
    nik = models.CharField(max_length=16, unique=True, verbose_name='NIK')
    date_of_birth = models.DateField(verbose_name='Tanggal Lahir')
    gender = models.CharField(max_length=1, choices=Gender.choices, verbose_name='Jenis Kalamin')
    address = models.TextField(verbose_name='Alamat')
    phone = models.CharField(max_length=20, blank=True, verbose_name='No. Telepon')
    blood_type = models.CharField(
        max_length=3,
        choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')],
        blank=True,
        verbose_name='Golongan Darah'
    )
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name='Kontak Darurat')
    emergency_phone = models.CharField(max_length=20, blank=True, verbose_name='No. Kontak Darurat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patients_patient'
        verbose_name = 'Pasien'
        verbose_name_plural = 'Pasien-pasien'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} (NIK: {self.nik})"

    @property
    def age(self):
        """Umur pasien dumasar tanggal lahir."""
        today = timezone.now().date()
        return (
            today.year - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )

    @property
    def name(self):
        """Alias pikeun compatibility."""
        return self.user.get_full_name()
