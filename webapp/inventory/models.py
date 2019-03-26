
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from profiles.models import Customer, Employee


class Service(models.Model):
    service = models.TextField(max_length=36, verbose_name=_('Service description'))
    cost = models.FloatField(help_text=_('Cost'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Date of creation'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Date of the last update'))

    def __str__(self):
        return self.service


class Device(models.Model):
    CHOICES_ESTATUS = (
        ('almacenado', 'Almacenado'),
        ('diagnosticado', 'Diagnosticado'),
        ('reparado', 'Reparado'),
        ('entregado', 'Entregado'),
    )
    folio = models.AutoField(primary_key=True)

    kind = models.CharField(max_length=22, verbose_name=_('Device type'))
    make = models.CharField(max_length=16, verbose_name=_('device make'))
    model = models.CharField(max_length=16, verbose_name=_('Device model'))

    status = models.CharField(max_length=13, default='almacenado', choices=CHOICES_ESTATUS)
    income_date = models.DateField(default=datetime.now, help_text=_('Device income date'))
    delivery_date = models.DateField(help_text=_('Tentative date of delivery device'))

    services = models.ManyToManyField(Service, help_text=_('Applied services'))

    total = models.FloatField(default=0.0, verbose_name=_('Total cost'))

    customer = models.ForeignKey(Customer, on_delete='PROTECT', help_text=_('Device owner'))
    assigned_to = models.ForeignKey(Employee, on_delete='PROTECT', help_text=_('Employye assigned to the device'))

    added_by = models.ForeignKey(User, on_delete='PROTECT', verbose_name='Added by', help_text=_('User tha added the device'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Date of creation'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Date of the last update'))

    def __unicode__(self):
        return '%s %s' % (self.kind, self.make)


class Payment(models.Model):
    service = models.CharField(max_length=16)
    amount = models.FloatField()
    payment_date = models.DateField(default=datetime.now, help_text=_('Payment date'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Date of creation'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Date of the last update'))

    def __unicode__(self):
        return self.service
