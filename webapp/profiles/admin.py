
from django.contrib import admin

from inventory.models import Device
from .models import Customer, Employee


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0


class CustomerAdmin(admin.ModelAdmin):

    list_display = ('surnames', 'names', 'phone')
    list_filter = ('created_at',)

    fieldsets = (
        ('Personal information',
            {'fields': ('names', 'surnames', 'phone', 'email', 'rfc', 'address')}),
        ('Additional information',
            {'fields': ('created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at')

    search_fields = ('email', 'surnames',)
    ordering = ('surnames', 'email')
    filter_horizontal = ()

    inlines = [
        DeviceInline,
    ]

class EmployeeAdmin(admin.ModelAdmin):

    list_display = ('surnames', 'names', 'phone')
    list_filter = ('created_at', 'is_active',)

    fieldsets = (
        ('Personal information',
            {'fields': ('names', 'surnames', 'phone', 'email', 'address')}),
        ('Salary information',
            {'fields': ('base_salary', 'percentage',)}),
        ('Additional information',
            {'fields': ('is_active', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at')

    search_fields = ('email', 'surnames',)
    ordering = ('surnames', 'email')
    filter_horizontal = ()

    inlines = [
        DeviceInline,
    ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
