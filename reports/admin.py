from django.contrib import admin
from .models import VisitReport, DoctorPerformance


@admin.register(VisitReport)
class VisitReportAdmin(admin.ModelAdmin):
    list_display = ['report_date_start', 'report_date_end', 'total_visits', 'completed_visits', 'revenue']
    list_filter = ['report_date_end']
    search_fields = ['report_date_start', 'report_date_end']
    readonly_fields = ['created_at']


@admin.register(DoctorPerformance)
class DoctorPerformanceAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'report_month', 'total_appointments', 'completed_appointments', 'total_revenue', 'patient_satisfaction']
    list_filter = ['report_month']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name']
