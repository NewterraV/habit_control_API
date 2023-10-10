import json
from datetime import datetime, timedelta
from typing import Any
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from habit.models import Habit


def create_periodic_task(habit_pk: int):
    """
    Метод получает экземпляр привычки и на основе его атрибутов создает периодическую задачу.
    :param habit_pk: Экземпляр модели Habit
    :return: None
    """
    now = datetime.utcnow()
    habit = Habit.objects.get(pk=habit_pk)
    start_time = datetime.combine(now.date(), habit.start_time)
    schedule, create = IntervalSchedule.objects.get_or_create(every=habit.period, period=IntervalSchedule.DAYS)

    task = PeriodicTask.objects.create(
        name=f'task/{habit.name}/{habit.pk}/{habit.period}',
        task='habit.tasks.task_send_telegram_message',
        interval=schedule,
        kwargs=json.dumps(
            {'telegram': habit.owner.telegram,
             'place': habit.place,
             'action': habit.action,
             'lide_time': habit.lide_time
             }
        ),
        start_time=start_time if habit.start_time > now.time() else start_time + timedelta(days=1),
    )
    task.save()
    habit.task = task.pk
    habit.save()


def delete_periodic_task(pk):
    """
    Метод удаляет периодическую задачу
    :param pk:
    :return:
    """
    task = PeriodicTask.objects.filter(pk=pk).first()
    task.delete()


def send_telegram_message(telegram, place, action, lide_time):
    """
        Метод отправки телеграм уведомления.
        :param telegram: id телеграм пользователя
        :param place: место выполнения задачи
        :param action: действие
        :param lide_time: время за которое необходимо выполнить задачу
        :return: None
        """
    print(f'Я выполнилась{telegram} {place} {action} {lide_time}')
