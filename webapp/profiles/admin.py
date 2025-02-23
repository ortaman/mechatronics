
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from inventory.models import Device
from .models import Customer, Employee


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0

    verbose_name = 'Dispositivo'
    verbose_name_plural = 'Dispositivos'

    fields  = (
        'folio', 'kind', 'status', 'income_date', 'delivery_date', 
        'services','investment', 'final_cost', 'to_collect'
    )

    """
    class Media:
        css = {
            'all': ('css/custom_admin.css',)  # Include custom CSS
        }
        js = ('js/custom_admin.js',)  # Include custom JavaScript
    """

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


class DeviceCustomerInline(DeviceInline):
    pass


class DeviceEmployeeInline(DeviceInline):
    fk_name = "assigned_to"


class CustomerAdmin(admin.ModelAdmin):

    list_display = ('surnames', 'names', 'phone', 'email')
    list_filter = ('created_at',)

    search_fields = ('email', 'surnames', 'names')
    ordering = ('surnames', 'email')

    fieldsets = (
        ('Personal information',
            {'fields': ('names', 'surnames', 'phone', 'email', 'rfc', 'address')}),
        ('Additional information',
            {'fields': ('created_at', 'updated_at',)}),
    )

    readonly_fields = ('created_at', 'updated_at')

    inlines = [
        DeviceCustomerInline,
    ]

    def has_delete_permission(self, request, obj=None):
        return False


class EmployeeAdmin(UserAdmin):

    list_display = ('username', 'surnames', 'names', 'phone', 'email', 'base_salary', 'is_staff', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_active',)

    search_fields = ('email', 'surnames', 'names')
    ordering = ('surnames', 'email')

    filter_horizontal = ('groups',)

    fieldsets = (
        ('Autenticación',
            {'fields': ('username', 'password')}),
        ('Personal information',
            {'fields': ('names', 'surnames', 'phone', 'email', 'address')}),
        ('Salary information',
            {'fields': ('base_salary', 'percentage',)}),
        ('Permisions',
            {'fields': ("is_staff", "is_active", "is_superuser", "groups")}),
        ('Additional information',
            {'fields': ('created_at', 'updated_at', 'last_login')}),
    )

    readonly_fields = ('is_superuser', 'created_at', 'updated_at', 'last_login')

    inlines = [
        DeviceEmployeeInline,
    ]

    def has_delete_permission(self, request, obj=None):
        return False
    

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
