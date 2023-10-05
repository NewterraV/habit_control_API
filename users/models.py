from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


NULLABLE = {
    'blank': True,
    'null': True
}


class User(AbstractUser):
    """
    Модель пользователя
    """

    first_name = models.CharField(max_length=150, verbose_name=_('first name'))
    last_name = models.CharField(max_length=150, verbose_name=_('last name'))
    email = models.EmailField(unique=True, verbose_name=_('email'))
    telegram = models.CharField(max_length=150, verbose_name=_('telegram id'), **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
