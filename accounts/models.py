from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """User model custom kalayan role (admin, dokter, staff, pasien)."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrator'
        DOKTER = 'dokter', 'Dokter'
        STAFF = 'staff', 'Staff'
        PASIEN = 'pasien', 'Pasien'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PASIEN)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_customuser'
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Para Pengguna'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    @property
    def last_login_time(self):
        return self.last_login or self.created_at


class PasswordResetToken(models.Model):
    """Token pikeun reset password."""
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='reset_token')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'accounts_passwordresettoken'
        verbose_name = 'Token Reset Password'
        verbose_name_plural = 'Token Reset Password'
    
    def __str__(self):
        return f"{self.user} - {self.token[:8]}..."
    
    def is_expired(self):
        return timezone.now() > self.expires_at
