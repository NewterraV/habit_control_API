from celery import shared_task

from habit.models import Habit
from habit.src.telegram_api import TelegramAPI
from habit.src.periodic_tusks import HabitPeriodicTask


@shared_task
def task_send_telegram_message(chat_id, text) -> None:
    """
    Отложенная задача по отправке телеграм уведомления
    :param chat_id: id телеграм пользователя
    :param text: сообщение
    :return: str
    """
    telegram = TelegramAPI()
    status = telegram.send_message(chat_id, text)
    return status


@shared_task
def task_get_telegram_id():
    """Задача проверяет обновления и на их основе определяет ID чата
    телеграм конкретного пользователя"""
    telegram = TelegramAPI()
    result = telegram.get_chat_id()
    return result


@shared_task
def task_create_periodic_task(habit_pk):
    """
    Отложенная задача получает экземпляр привычки и на основе его атрибутов
    создает периодическую задачу. Возвращает pk
    периодической задачи.
    :param habit_pk: Экземпляр модели Habit
    :return: PK созданной периодической задачи
    """
    task = HabitPeriodicTask(habit_pk)
    task.create_periodic_task()


@shared_task
def task_update_periodic_task(habit_pk):
    """
    Отложенная задача обновляет модель периодической задачи
    :param habit_pk: id экземпляра модели Habit
    :return: str
    """
    task = HabitPeriodicTask(habit_pk)
    task.update_periodic_task()


@shared_task
def task_delete_periodic_task(pk):
    """
    Отложенная задача удаляет периодическую задачу
    :param pk: PK задачи
    :return: None
    """
    task = HabitPeriodicTask()
    task.delete_periodic_task(pk)
