import binascii
import os

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('Email address'), unique=True, max_length=255)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CustomToken(models.Model):
    key = models.CharField(_('Key'), max_length=100, primary_key=True)
    user = models.OneToOneField(
        CustomUser, related_name='authentication_token',
        on_delete=models.CASCADE, verbose_name=_('User')
    )
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        verbose_name = _('CustomToken')
        verbose_name_plural = _('CustomTokens')

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return f"{self.key} - ({self.user.email})"