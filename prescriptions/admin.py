from django.contrib import admin
from .models import Medicine, Prescription, PrescriptionItem


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 0
    readonly_fields = ['medicine', 'dosage', 'frequency', 'duration', 'quantity']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'generic_name', 'form', 'manufacturer', 'price', 'stock', 'is_active']
    list_filter = ['form', 'is_active']
    search_fields = ['name', 'generic_name', 'manufacturer']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informasi Obat', {'fields': ('name', 'generic_name', 'form', 'manufacturer')}),
        ('Harga & Stok', {'fields': ('unit', 'price', 'stock', 'expiry_date')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamp', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['get_patient', 'appointment', 'diagnosis', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['appointment__patient__user__first_name', 'appointment__patient__user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PrescriptionItemInline]

    fieldsets = (
        ('Informasi Resep', {'fields': ('appointment', 'status')}),
        ('Diagnosa & Pengobatan', {'fields': ('diagnosis', 'treatment_notes')}),
        ('Timestamp', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Pasien')
    def get_patient(self, obj):
        return obj.appointment.patient


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'medicine', 'dosage', 'frequency', 'duration', 'quantity']
    list_filter = ['prescription__status']
    search_fields = ['medicine__name']
