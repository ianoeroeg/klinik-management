from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['get_patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'priority']
    list_filter = ['status', 'priority', 'appointment_date']
    search_fields = ['patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name']
    date_hierarchy = 'appointment_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informasi Appointment', {'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time')}),
        ('Status & Prioritas', {'fields': ('status', 'priority')}),
        ('Detail', {'fields': ('reason', 'notes')}),
        ('Timestamp', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Pasien')
    def get_patient(self, obj):
        return obj.patient
