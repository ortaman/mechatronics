
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    names = models.CharField(max_length=32)
    surnames = models.CharField(max_length=32)

    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=64, blank=True, null=True)

    rfc = models.CharField(max_length=13, blank=True, null=True, verbose_name='RFC')

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Date of creation'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Date of the last update'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        unique_together = ('names', 'surnames', )

    def __str__(self):
        return '%s %s' % (self.names, self.surnames, )


class Employee(models.Model):
    names = models.CharField(max_length=32)
    surnames = models.CharField(max_length=32)

    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=64, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    base_salary = models.FloatField(verbose_name=_('Base Salary'))
    percentage = models.FloatField(verbose_name=_('Commission percentage'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Date of creation'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Date of the last update'))

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        unique_together = ('names', 'surnames',)

    def __str__(self):
        return '%s %s' % (self.names, self.surnames, )
