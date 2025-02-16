
from django.db import models
from django.contrib import admin
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from .models import Device, PaymentDevice, PaymentPayroll, PaymentService, Service


class PaymentDeviceInline(admin.TabularInline):
    model = PaymentDevice
    extra = 0

    verbose_name = 'Pago del Cliente'
    verbose_name_plural = 'Pagos del Cliente'

    fields  = ('payment_type', 'amount', 'payment_date', 'device', 'added_by')

    readonly_fields = ('payment_date', 'created_at', 'updated_at', 'added_by')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DeviceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(
                attrs={
                    'rows': 1,
                    'cols': 50,
                    'style': 'height: 10em;'
                }
            )
        },
    }

    # raw_id_fields = ('customer',)
    date_hierarchy = 'income_date'

    list_display = ('folio', 'customer', 'kind', 'status', 'income_date', 'tentative_delivery_date', 'delivery_date', 'assigned_to')
    list_filter = ('income_date', 'delivery_date',)

    autocomplete_fields = ('customer',)

    fieldsets = (
        ('Información del dispositivo',
            {
                'fields': (('folio',),
                           ('kind', 'make', 'model', 'sn', 'extras', 'status'),
                           ('big_risk',),  
                           'income_date', 'tentative_delivery_date', 'delivery_date', 
                           ('client_inf', 'services', 'extra_info'), 
                           ('quote', 'investment', 'final_cost'), ('paid', 'to_collect'),
                           'customer', 'assigned_to', 
        ), "classes": [""],}),
        ('Additional Information',
            {
                'fields': (
                    ('ultimatum_notification', 'ultimatum_date'),
                    'added_by', 'created_at', 'updated_at',
                )
            }
        ),
    )

    readonly_fields = (
        'folio', 'income_date', 'tentative_delivery_date', 'paid', 'to_collect', 'created_at', 'updated_at', 'added_by'
    )

    search_fields = ('folio', 'kind', 'status', 'customer__surnames')
    ordering = ('delivery_date',)

    inlines = [
        PaymentDeviceInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(DeviceAdmin, self).get_form(request, obj, **kwargs)
        
        field = form.base_fields["customer"]
        field.widget.can_delete_related = False

        field = form.base_fields["assigned_to"]

        field.widget.can_delete_related = False
        field.widget.can_change_related = False
        field.widget.can_add_related = False
        field.widget.can_view_related = False

        return form

    def save_formset(self, request, form, formset, change):

        total_amount = 0
        instances = formset.save(commit=False)

        for instance in instances:
            total_amount += instance.amount
            
            if not instance.pk:
                instance.added_by = request.user
            instance.save()
        
        self.total_amount = total_amount
        formset.save_m2m()

    def save_model(self, request, obj, form, change):

        if hasattr(self, 'total_amount'):
            obj.paid += self.total_amount

        if obj.final_cost:
            obj.to_collect = obj.final_cost - obj.paid
        
        obj.added_by = request.user
        super().save_model(request, obj, form, change)


class PaymentPayrollAdmin(admin.ModelAdmin):

    list_display = ('employee', 'amount', 'payment_date')
    list_filter = ('payment_date', 'employee')

    fieldsets = (
        ('Información del Pago',
            {'fields': ('employee', 'amount', 'payment_date')}),
        ('Información Adicional',
            {'fields': ('created_at', 'updated_at')})
    )

    readonly_fields = ('created_at', 'updated_at')

    # search_fields = ('service',)
    ordering = ('created_at',)
    filter_horizontal = ()

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False

        return formfield
    
    def get_queryset(self, request):
       queryset = super(PaymentPayrollAdmin, self).get_queryset(request)
       queryset = queryset.filter(employee__isnull=False)
       return queryset
    

class PaymentServiceAdmin(admin.ModelAdmin):

    list_display = ('service', 'amount', 'payment_date')
    list_filter = ('payment_date',)

    fieldsets = (
        ('Información del Pago',
            {'fields': ('service', 'amount', 'payment_date')}),
        ('Información Adicional',
            {'fields': ('created_at', 'updated_at')})
    )

    readonly_fields = ('created_at', 'updated_at')

    # search_fields = ('service',)
    ordering = ('created_at',)
    filter_horizontal = ()

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False

        return formfield

    def get_queryset(self, request):
       queryset = super(PaymentServiceAdmin, self).get_queryset(request)
       queryset = queryset.filter(employee__isnull=True)
       return queryset
    

class PaymentDeviceAdmin(admin.ModelAdmin):

    list_display = ('payment_type', 'amount', 'payment_date', 'device', 'added_by')
    list_filter = ('payment_date',)

    fieldsets = (
        ('Información del Pago',
            {
                'fields': ('payment_type', 'amount', 'payment_date', 'device', 'added_by')
            }
        ),
        ('Información Adicional',
            {
                'fields': ('created_at', 'updated_at')
            }
        )
    )

    readonly_fields = ('added_by', 'created_at', 'updated_at')

    search_fields = ('device__customer__names', 'device__customer__surnames')
    ordering = ('created_at',)
    # filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    """
    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        # formfield.widget.can_add_related = False
        # formfield.widget.can_view_related = False

        return formfield
    """


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

    fieldsets = (
        ('Información del Pago',
            {
                'fields': ('name', 'description')
            }
        ),
        ('Información Adicional',
            {
                'fields': ('created_at', 'updated_at')
            }
        )
    )

    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    

admin.site.register(Device, DeviceAdmin)

admin.site.register(PaymentPayroll, PaymentPayrollAdmin)
admin.site.register(PaymentService, PaymentServiceAdmin)


admin.site.register(PaymentDevice, PaymentDeviceAdmin) # Changes to CustomerPayment

admin.site.register(Service, ServiceAdmin)
