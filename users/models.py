from random import randint

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

    username = None
    first_name = models.CharField(max_length=150, verbose_name=_('first name'))
    last_name = models.CharField(max_length=150, verbose_name=_('last name'))
    email = models.EmailField(unique=True, verbose_name=_('email'))
    telegram = models.CharField(max_length=150, verbose_name=_('telegram id'), **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name=_('active'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Verify(models.Model):
    """
    Модель для проверки кода верификации пользователя
    """
    user_code = models.PositiveIntegerField(max_length=5, verbose_name=_('user code'), **NULLABLE)
    verify_code = models.PositiveIntegerField(default=randint(00000, 99999), verbose_name=_('verify code'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'), related_name='verify')
