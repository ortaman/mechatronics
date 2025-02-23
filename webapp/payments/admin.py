from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from profiles.models import Employee
from payments.models import PayrollPayment, ServicePayment, CustomerPayment, ProductPayment


class PayrollPaymentAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            kwargs["queryset"] = Employee.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = ('employee', 'amount', 'payment_date')
    list_filter = ('payment_date',)

    search_fields = ('employee__email', 'employee__surnames', 'employee__names')
    ordering = ('created_at',)

    fieldsets = (
        ('Información del Pago',
            {'fields': ('employee', 'amount', 'payment_date')}),
        ('Información Adicional',
            {'fields': ('created_at', 'updated_at')})
    )

    readonly_fields = ('payment_date', 'added_by', 'created_at', 'updated_at')

    def has_delete_permission(self, request, obj=None):
        return False

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False

        return formfield
    
    def get_queryset(self, request):
       queryset = super(PayrollPaymentAdmin, self).get_queryset(request)
       queryset = queryset.filter(payment_type='nomina')
       return queryset

    def save_model(self, request, obj, form, change):
        obj.payment_type = 'nomina'
        obj.added_by = request.user
        super().save_model(request, obj, form, change)    


class ServicePaymentAdmin(admin.ModelAdmin):

    list_display = ('service', 'amount', 'payment_date')
    list_filter = ('payment_date',)

    search_fields = ('service__name',)
    ordering = ('created_at',)

    fieldsets = (
        ('Información del Pago',
            {'fields': ('service', 'amount', 'payment_date')}),
        ('Información Adicional',
            {'fields': ('created_at', 'updated_at')})
    )

    readonly_fields = ('payment_date', 'added_by', 'created_at', 'updated_at')

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False
        formfield.widget.can_view_related = False

        return formfield

    def get_queryset(self, request):
       queryset = super(ServicePaymentAdmin, self).get_queryset(request)
       queryset = queryset.filter(payment_type='servicio')
       return queryset

    def save_model(self, request, obj, form, change):
        obj.payment_type = 'servicio'
        obj.added_by = request.user
        super().save_model(request, obj, form, change)


class CustomerPaymentAdmin(admin.ModelAdmin):
    
    list_display = ('device', 'device__customer', 'amount', 'payment_date', 'added_by')
    list_filter = ('payment_date',)

    search_fields = ('device__folio', 'device__customer__names', 'device__customer__surnames')
    ordering = ('created_at',)

    autocomplete_fields = ('device',)

    fieldsets = (
        ('Información del Pago',
            {
                'fields': ('device', 'amount', 'payment_date', 'added_by')
            }
        ),
        ('Información Adicional',
            {
                'fields': ('created_at', 'updated_at')
            }
        )
    )

    readonly_fields = ('payment_date', 'added_by', 'created_at', 'updated_at')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
       queryset = super(CustomerPaymentAdmin, self).get_queryset(request)
       queryset = queryset.filter(payment_type='cliente')
       return queryset

    def save_model(self, request, obj, form, change):
        obj.payment_type = 'cliente'
        obj.added_by = request.user
        super().save_model(request, obj, form, change)   


class ProductPaymentAdmin(admin.ModelAdmin):

    list_display = ('id', 'product', 'amount', 'payment_date', 'added_by', 'payment_type')
    list_display_links = ('id', 'product',)

    list_filter = ('payment_date',)

    search_fields = ('product__pk', 'product__name')
    ordering = ('created_at',)

    autocomplete_fields = ('product',)

    fieldsets = (
        ('Información del Pago',
            {
                'fields': ('product','amount', 'payment_date', 'added_by')
            }
        ),
        ('Información Adicional',
            {
                'fields': ('created_at', 'updated_at')
            }
        )
    )

    readonly_fields = ('payment_date', 'added_by', 'created_at', 'updated_at')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
       queryset = super(ProductPaymentAdmin, self).get_queryset(request)
       queryset = queryset.filter(payment_type='producto')
       return queryset

    def save_model(self, request, obj, form, change):
        obj.payment_type = 'producto'
        obj.added_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(PayrollPayment, PayrollPaymentAdmin)
admin.site.register(ServicePayment, ServicePaymentAdmin)

admin.site.register(CustomerPayment, CustomerPaymentAdmin)
admin.site.register(ProductPayment, ProductPaymentAdmin)
