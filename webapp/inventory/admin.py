
from django.db import models
from django.contrib import admin
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from inventory.models import Device, Product, Service
from payments.models import CustomerPayment, ProductPayment


class CustomerPaymentInline(admin.TabularInline):
    model = CustomerPayment
    extra = 0

    verbose_name = 'Pago del Cliente'
    verbose_name_plural = 'Pagos del Cliente'

    fields  = ('amount', 'payment_date', 'device', 'added_by')

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

    list_display = ('folio', 'kind', 'customer', 'status', 'income_date', 'tentative_delivery_date', 'delivery_date', 'assigned_to')
    list_display_links = ('folio', 'kind')

    list_filter = ('income_date', 'delivery_date',)

    search_fields = ('folio', 'kind', 'status', 'customer__surnames')
    ordering = ('delivery_date',)

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

    inlines = [
        CustomerPaymentInline,
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
        instances = formset.save(commit=False)

        for instance in instances:
            if not instance.pk:
                instance.added_by = request.user
            instance.save()
        
        formset.save_m2m()

    def save_model(self, request, obj, form, change):

        obj.added_by = request.user
        super().save_model(request, obj, form, change)
    

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')

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
    

class ProductAdminInline(admin.TabularInline):
    model = ProductPayment
    extra = 0

    verbose_name = 'Pago del Cliente'
    verbose_name_plural = 'Pagos del Cliente'

    fields  = ('amount', 'payment_date', 'product', 'added_by')

    readonly_fields = ('payment_date', 'created_at', 'updated_at', 'added_by')

    def has_delete_permission(self, request, obj=None):
        return False


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost', 'stock', 'sold', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')

    search_fields = ('id', 'name')
    ordering = ('stock',)

    fieldsets = (
        ('Información del Pago',
            {
                'fields': ('id', 'name', 'cost', 'stock', 'sold')
            }
        ),
        ('Información Adicional',
            {
                'fields': ('created_at', 'updated_at')
            }
        )
    )

    readonly_fields = ('id', 'created_at', 'updated_at')

    inlines = [
        ProductAdminInline,
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if not instance.pk:
                instance.added_by = request.user
            instance.save()
        
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        
        obj.added_by = request.user
        super().save_model(request, obj, form, change)
    

admin.site.register(Device, DeviceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Service, ServiceAdmin)
