from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
import io
import uuid

# Create your models here.


class TokenQr(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(
        default=False, verbose_name="Añadida A Un Usuario")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.token}'


class User(models.Model):
    token = models.OneToOneField(
        TokenQr,
        on_delete=models.CASCADE,
        verbose_name=_('Token Qr')
    )
    ci = models.CharField(_('Cedula'), max_length=8,
                          blank=False, null=False)
    name = models.CharField(_('Nombres'), max_length=50,
                                blank=False, null=False)
    last_name = models.CharField(
        _('Apellidos'), max_length=50, blank=False, null=False)
    address = models.TextField(_('Direccion'),)
    birthday = models.DateField(_('Fecha De Nacimiento'),)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name}'

    def get_full_name(self):
        return f'{self.name} {self.last_name}'

    def save(self, *args, **kwargs):
        token = self.token
        token.is_active = True
        token.save()
        return super(User, self).save(*args, **kwargs)
