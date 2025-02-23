from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from inventory.models import Device, Product, Service
from profiles.models import Employee


class Payment(models.Model):
    PAYMENT_TYPE = [
        ("nomina", "Nómina"),
        ("cliente", "Cliente"),
        ("servicio", "Servicio"),
        ("producto", "Producto"),
    ]

    payment_type = models.CharField(max_length=8, choices=PAYMENT_TYPE, verbose_name=_('Tipo de Pago'))

    amount = models.FloatField(verbose_name=_('Cantidad del pago'))
    payment_date = models.DateField(default=datetime.now, verbose_name=_('Fecha de pago'))

    device = models.ForeignKey(Device, on_delete=models.PROTECT, null=True, verbose_name=_('Dispositivo'))
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, verbose_name=_('Empleado'), related_name = 'employee')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, verbose_name=_('Servicio'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, verbose_name=_('Producto'))

    added_by = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name=_('Pago recibido por'), related_name = 'addedby')

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Fecha de la última actualización'))


class PayrollPayment(Payment):
    class Meta:
        proxy = True

        verbose_name = _('Pagos de Nómina')
        verbose_name_plural = _('Pagos de Nómina')


    def __str__(self):
        return f''


class ServicePayment(Payment):
    class Meta:
        proxy = True

        verbose_name = _('Pagos de Servicio')
        verbose_name_plural = _('Pagos de Servicios')

    def __str__(self):
        return f''


class CustomerPayment(Payment):
    class Meta:
        proxy = True

        verbose_name = _('Pagos a Reparacion')
        verbose_name_plural = _('Pagos a Reparaciones')

    def __str__(self):
        return f''
    
    def save(self):
        payments = CustomerPayment.objects.filter(device=self.device.pk)

        total_paid = 0
        for payment in payments:
            total_paid += payment.amount

        if self.amount:
            total_paid = total_paid + self.amount

        device = Device.objects.get(pk=self.device.pk)
        if device.final_cost:
            device.to_collect = device.final_cost - total_paid

        device.paid = total_paid
        device.save()

        self.payment_type = 'cliente'
        super(CustomerPayment, self).save()


class ProductPayment(Payment):
    class Meta:
        proxy = True

        verbose_name = _('Pagos a Producto')
        verbose_name_plural = _('Pagos a Productos')

    def __str__(self):
        return f''

    def save(self):
        product = Product.objects.get(pk=self.product.pk)
        product.sold += 1
        product.stock -= 1
        product.save()

        self.payment_type = 'producto'
        super(ProductPayment, self).save()
