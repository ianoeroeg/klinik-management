from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class UserActivityLog(models.Model):
    """Log aktivitas pikeun unggal pengguna."""
    
    class ActivityType(models.TextChoices):
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'
        CREATE = 'create', 'Ngarékam Data Anyar'
        UPDATE = 'update', 'Ngropéa Data'
        DELETE = 'delete', 'Ngahapus Data'
        VIEW = 'view', 'Ningali Data'
        CHANGE_PASSWORD = 'change_password', 'Ngarobah Password'
        ROLE_CHANGE = 'role_change', 'Ngarobah Role'
        
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'accounts_useractivitylog'
        verbose_name = 'Log Aktivitas'
        verbose_name_plural = 'Log Aktivitas'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.get_activity_type_display()} - {self.timestamp}"


class PasswordResetToken(models.Model):
    """Token pikeun reset password."""
    
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='reset_token')
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
