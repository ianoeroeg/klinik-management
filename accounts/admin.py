from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'get_full_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    readonly_fields = ['date_joined', 'last_login']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informasi Tambahan', {'fields': ('role', 'phone', 'avatar')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informasi Tambahan', {'fields': ('role', 'phone')}),
    )
