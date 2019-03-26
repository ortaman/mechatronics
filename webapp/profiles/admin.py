
from django.contrib import admin
from .models import Customer, Employee


class CustomerAdmin(admin.ModelAdmin):

    list_display = ('surnames', 'names', 'phone')
    list_filter = ('created_at',)

    fieldsets = (
        ('Información personal',
            {'fields': ('names', 'surnames', 'phone', 'email', 'rfc', 'address')}),
        ('Información adicional',
            {'fields': ('created_at', 'updated_at',)}),
    )

    readonly_fields = ('id', 'created_at', 'updated_at')

    search_fields = ('email', 'surnames',)
    ordering = ('surnames', 'email')
    filter_horizontal = ()


class EmployeeAdmin(admin.ModelAdmin):

    list_display = ('surnames', 'names', 'phone')
    list_filter = ('created_at', 'is_active',)

    fieldsets = (
        ('Información personal',
            {'fields': ('names', 'surnames', 'phone', 'email', 'address')}),
        ('Información salarial',
            {'fields': ('base_salary', 'percentage',)}),
        ('Información adicional',
            {'fields': ('is_active', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('id', 'created_at', 'updated_at')

    search_fields = ('email', 'surnames',)
    ordering = ('surnames', 'email')
    filter_horizontal = ()


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
