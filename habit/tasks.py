from celery import shared_task
from habit.services import send_telegram_message
from habit.src.periodic_tusks import HabitPeriodicTask


@shared_task
def task_send_telegram_message(telegram, place, action, lide_time) -> None:
    """
    Отложенная задача по отправке телеграм уведомления
    :param telegram: id телеграм пользователя
    :param place: место выполнения задачи
    :param action: действие
    :param lide_time: время за которое необходимо выполнить задачу
    :return: None
    """
    send_telegram_message(telegram, place, action, lide_time)


@shared_task
def task_create_periodic_task(habit_pk):
    """
    Отложенная задача получает экземпляр привычки и на основе его атрибутов
    создает периодическую задачу. Возвращает pk
    периодической задачи.
    :param habit_pk: Экземпляр модели Habit
    :return: PK созданной периодической задачи
    """
    habit = HabitPeriodicTask(habit_pk)
    habit.create_periodic_task()


@shared_task
def task_update_periodic_task(habit_pk):
    """
    Отложенная задача обновляет модель периодической задачи
    :param habit_pk: id экземпляра модели Habit
    :return: None
    """
    habit = HabitPeriodicTask(habit_pk)
    habit.update_periodic_task()


@shared_task
def task_delete_periodic_task(pk):
    """
    Отложенная задача удаляет периодическую задачу
    :param pk: PK задачи
    :return: None
    """
    habit = HabitPeriodicTask()
    habit.delete_periodic_task(pk)
