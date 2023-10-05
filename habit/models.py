from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

from users.models import User, NULLABLE


class HabitPeriod(models.TextChoices):
    """
    Класс описывает экземпляры для выбора периода
    """
    ONE_DAY = (timedelta(days=1), _('One day'))
    TWO_DAY = (timedelta(days=2), _('Two days'))
    THREE_DAY = (timedelta(days=3), _('Three days'))
    FOUR_DAY = (timedelta(days=4), _('Four days'))
    FIVE_DAY = (timedelta(days=5), _('Five days'))
    SIX_DAY = (timedelta(days=6), _('Six days'))
    SEVEN_DAY = (timedelta(days=7), _('Seven days'))


class Habit(models.Model):
    """
    Класс модели привычки
    """

    name = models.CharField(max_length=150, verbose_name=_('name'))
    place = models.CharField(max_length=200, verbose_name=_('place'))
    action = models.TextField(verbose_name=_('action'))
    start_time = models.TimeField(verbose_name=_('start time'))
    lide_time = models.TimeField(verbose_name=_('lead time'))
    period = models.TimeField(choices=HabitPeriod.choices, verbose_name=_('period'), default=HabitPeriod.ONE_DAY)
    is_nice = models.BooleanField(verbose_name=_('sign of a pleasant habit'), **NULLABLE)
    is_publish = models.BooleanField(verbose_name=_('is publish'), **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('owner'), related_name='habit')

    class Meta:
        verbose_name = _('habit')
        verbose_name_plural = _('habits')


class Nice(models.Model):
    """
    Класс субмодели приятной привычки
    """

    habit = models.OneToOneField(Habit, on_delete=models.CASCADE, related_name='nise', verbose_name=_('habit'))

    class Meta:
        verbose_name = _('nice_habit')
        verbose_name_plural = _('nice_habits')


class Useful(models.Model):
    """
    Класс субмодели привычки
    """

    nice = models.ForeignKey(Nice, on_delete=models.SET_NULL, verbose_name=_('habit'), related_name='nise', **NULLABLE)
    reward = models.TextField(verbose_name=_('reward'), **NULLABLE)
    habit = models.OneToOneField(Habit, on_delete=models.CASCADE, verbose_name=_('habit'), related_name='useful')

    class Meta:
        verbose_name = _('useful_habit')
        verbose_name_plural = _('useful_habits')
