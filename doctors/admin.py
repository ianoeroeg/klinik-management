from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'license_number', 'specialization', 'consultation_fee', 'is_available']
    list_filter = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'license_number']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informasi Pengguna', {'fields': ('user',)}),
        ('Informasi Profesi', {'fields': ('license_number', 'specialization', 'education', 'experience_years')}),
        ('Biaya & Ketersediaan', {'fields': ('consultation_fee', 'is_available')}),
        ('Timestamp', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Ngaran')
    def get_full_name(self, obj):
        return obj.user.get_full_name()
