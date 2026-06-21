from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'nik', 'gender', 'age', 'phone', 'created_at']
    list_filter = ['gender', 'blood_type', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'nik', 'phone']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informasi Pengguna', {'fields': ('user',)}),
        ('Informasi Pribadi', {'fields': ('nik', 'date_of_birth', 'gender', 'blood_type')}),
        ('Kontak & Alamat', {'fields': ('address', 'phone', 'emergency_contact', 'emergency_phone')}),
        ('Timestamp', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Ngaran')
    def get_full_name(self, obj):
        return obj.user.get_full_name()
