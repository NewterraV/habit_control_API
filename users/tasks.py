from celery import shared_task

from habit.models import Habit
from habit.src.periodic_tusks import HabitPeriodicTask
from users.services import send_verify


@shared_task
def task_send_verify(verify_pk: int) -> None:
    """
    Отложенная задача отправляет письмо с кодом верификации
    :param verify_pk: ID модели верификации
    :return: None
    """
    send_verify(verify_pk)


@shared_task
def task_multiple_update_periodic_task(user_id):
    """Метод обновляет все периодические задачи на основе
    привычек пользователя"""
    habits = Habit.objects.filter(owner=user_id)
    if not habits:
        return
    for habit in habits:
        task = HabitPeriodicTask(habit_pk=habit.pk)
        task.update_periodic_task()
