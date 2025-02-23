
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models import Customer, Employee


class Device(models.Model):

    CHOICES_ESTATUS = (
        ('almacenado', 'Almacenado'),
        ('diagnosticado', 'Diagnosticado'),
        ('reparado', 'Reparado'),
        ('entregado', 'Entregado'),
        ('reingreso', 'Reingreso'),
        ('cancelado', 'Cancelado'),
    )
    folio = models.AutoField(primary_key=True)

    kind = models.CharField(max_length=24, verbose_name=_('Tipo del dispositivo'))
    make = models.CharField(max_length=16, verbose_name=_('Marca del dispositivo'))
    model = models.CharField(max_length=16, verbose_name=_('Modelo del dispositivo'))
    sn = models.CharField(max_length=16, verbose_name=_('Número de serie'))
    big_risk = models.BooleanField(default=False, verbose_name=_('Reparación de alto riesgo'))

    extras = models.CharField(max_length=16, blank=True, null=True, verbose_name=_('Dispositivos extras'))

    status = models.CharField(max_length=13, default='almacenado', choices=CHOICES_ESTATUS)
    income_date = models.DateField(default=datetime.now, verbose_name=_('Fecha de ingreso'))
    
    tentative_delivery_date = models.DateField(blank=True, null=True, verbose_name=_('Fecha tentativa de entrega'))
    delivery_date = models.DateField(blank=True, null=True, verbose_name=_('Fecha de entrega'))

    client_inf = models.TextField(verbose_name=_('Falla reportada por el cliente'))
    services = models.TextField(blank=True, null=True, verbose_name=_('Servicios aplicados'))
    extra_info = models.TextField(blank=True, null=True, verbose_name=_('Observaciones'))

    quote = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_('Cotización'))
    investment = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_('Pago de refacciones'))
    
    final_cost = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_('Costo final'))
    paid = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_('Pagos'))
    to_collect = models.FloatField(default=0.0, blank=True, null=True, verbose_name=_('Por cobrar'))

    ultimatum_notification = models.BooleanField(default=False, verbose_name=_('Ultimatum Notificado'))
    ultimatum_date = models.DateField(blank=True, null=True, verbose_name=_('Fecha del Ultimatum'))

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_('Cliente'))
    assigned_to = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.PROTECT, related_name='assigned_to', verbose_name=_('Empleado asignado'))

    added_by = models.ForeignKey(Employee, blank=True, on_delete=models.PROTECT, related_name='added_by', verbose_name=_('Empleado quien agregó el dispositivo'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Fecha de la última actualización'))

    class Meta:
        verbose_name = _('Dispositivo')
        verbose_name_plural = _('Dispositivos')

    def __str__(self):
        return f'{self.folio} - {self.kind} - {self.make}'


class Service(models.Model):

    name = models.CharField(max_length=24,  verbose_name=_('Nombre del servicio'))
    description = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Descripción'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Fecha de la última actualización'))

    class Meta:
        verbose_name = _('Servicio')
        verbose_name_plural = _('Servicios')

    def __str__(self):
        return  f'{self.name}'


class Product(models.Model):

    name = models.CharField(max_length=40, verbose_name=_('Nombre del producto'))
    cost = models.FloatField(verbose_name=_('Costo del producto'))

    stock = models.IntegerField(verbose_name=_('Existencias'))
    sold = models.IntegerField(default=0, verbose_name=_('Vendidos'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Fecha de la última actualización'))

    def __str__(self):
        return f'{self.name}'
