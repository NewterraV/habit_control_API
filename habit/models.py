from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User, NULLABLE


class HabitPeriod(models.TextChoices):
    """
    Класс описывает экземпляры для выбора периода
    """
    ONE_DAY = (1, _('One day'))
    TWO_DAY = (2, _('Two days'))
    THREE_DAY = (3, _('Three days'))
    FOUR_DAY = (4, _('Four days'))
    FIVE_DAY = (5, _('Five days'))
    SIX_DAY = (6, _('Six days'))
    SEVEN_DAY = (7, _('Seven days'))


class Habit(models.Model):
    """
    Класс модели привычки
    """

    name = models.CharField(max_length=150, verbose_name=_('name'),)
    place = models.CharField(max_length=200, verbose_name=_('place'))
    action = models.TextField(verbose_name=_('action'))
    start_time = models.TimeField(verbose_name=_('start time'))
    lide_time = models.IntegerField(verbose_name=_('lead time'))
    period = models.PositiveIntegerField(choices=HabitPeriod.choices, verbose_name=_('period'),
                                         default=HabitPeriod.ONE_DAY)
    is_publish = models.BooleanField(verbose_name=_('is publish'), **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('owner'), related_name='habit')

    def __str__(self):
        return f'{self.name} - {self.period}'

    class Meta:
        verbose_name = _('habit')
        verbose_name_plural = _('habits')
        ordering = ['name']


class Nice(models.Model):
    """
    Класс субмодели приятной привычки
    """

    habit = models.OneToOneField(Habit, on_delete=models.CASCADE, related_name='nise', verbose_name=_('habit'))

    def __str__(self):
        return f'{self.habit.name}'

    class Meta:
        verbose_name = _('nice_habit')
        verbose_name_plural = _('nice_habits')


class Reward(models.Model):
    """
    Класс субмодели привычки
    """
    is_nice = models.BooleanField(verbose_name=_('sign of a pleasant habit'), **NULLABLE)
    nice = models.ForeignKey(Nice, on_delete=models.SET_NULL, verbose_name=_('habit'), related_name='nice', **NULLABLE)
    reward = models.TextField(verbose_name=_('reward'), **NULLABLE)
    habit = models.OneToOneField(Habit, on_delete=models.CASCADE, verbose_name=_('habit'), related_name='reward',
                                 **NULLABLE)

    def __str__(self):
        return f'{self.habit.name} - {self.reward if self.reward else self.nice if not self.is_nice else self.is_nice}'

    class Meta:
        verbose_name = _('useful_habit')
        verbose_name_plural = _('useful_habits')
