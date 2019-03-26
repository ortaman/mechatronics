
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Service, Device, Payment


class ServiceAdmin(admin.ModelAdmin):

    list_display = ('service', 'cost',)
    list_filter = ('created_at',)

    fieldsets = (
        ('Service Information',
            {'fields': ('service', 'cost',)}),
    )

    readonly_fields = ('created_at', 'updated_at')

    search_fields = ('service',)
    ordering = ('created_at',)
    filter_horizontal = ()


class ServicesInline(admin.TabularInline):
    model = Device.services.through
    extra = 1


class DeviceAdmin(admin.ModelAdmin):

    # date_hierarchy = ('income_date')
    # raw_id_fields = ('customer',)
    list_display = ('folio', 'customer', 'kind', 'status', 'income_date', 'delivery_date', 'assigned_to')
    list_filter = ('income_date', 'delivery_date',)

    fieldsets = (
        (_('Device Information'),
            {'fields': ('folio', 'kind', 'make', 'model', 'status', 'income_date',
                        'delivery_date', 'services', 'total', 'customer')}),
        ('Additional Information',
            {'fields': ('added_by', 'created_at', 'updated_at',)}),
    )

    readonly_fields = ('folio', 'created_at', 'updated_at')

    search_fields = ('service',)
    ordering = ('delivery_date',)
    # filter_horizontal = ('services',)

    inlines = [
        ServicesInline,
    ]


class PaymentAdmin(admin.ModelAdmin):

    list_display = ('service', 'amount', 'payment_date')
    list_filter = ('payment_date',)

    fieldsets = (
        ('Payment information',
            {'fields': ('service', 'amount', 'payment_date')}),
    )

    readonly_fields = ('created_at', 'updated_at')

    search_fields = ('service',)
    ordering = ('payment_date',)
    filter_horizontal = ()


admin.site.register(Service, ServiceAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Payment, PaymentAdmin)
