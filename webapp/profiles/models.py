
from django.db import models
from django.utils.translation import gettext_lazy as _


from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password, make_password

from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=128,
        unique=True,
        help_text=_('Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(max_length=128, verbose_name=_('email'))
    names = models.CharField(max_length=64, verbose_name=_('names'))
    surnames = models.CharField(max_length=64, verbose_name=_('surnames'))

    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=64, blank=True, null=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('base_user')
        verbose_name_plural = _('base_users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.names, self.surnames)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.surnames

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Employee(AbstractUser):
    
    base_salary = models.FloatField(default=0, verbose_name=_('Base Salary'))
    percentage = models.FloatField(default=0, verbose_name=_('Commission percentage'))

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Fecha de la última actualización'))

    class Meta:
        verbose_name = _('Empleado')
        verbose_name_plural = _('Empleados')
        unique_together = ('names', 'surnames',)


    def __str__(self):
        return f"{self.get_full_name()}"


class Customer(models.Model):
    names = models.CharField(max_length=32)
    surnames = models.CharField(max_length=32)

    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=32, null=True, blank=True)

    address = models.CharField(max_length=64, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True, verbose_name='RFC')
    social_rfc = models.CharField(max_length=13, blank=True, null=True, verbose_name='Razón social')

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_('Fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Fecha de la última actualización'))

    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')
        unique_together = ('names', 'surnames', )

    def __str__(self):
        return f'{self.names} {self.surnames}'

