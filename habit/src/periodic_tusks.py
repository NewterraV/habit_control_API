import json
from datetime import datetime, timedelta
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from habit.models import Habit


class HabitPeriodicTask:

    def __init__(self, habit_pk=None):
        """
        Класс для работы с периодическими задачами
        :param habit_pk: id экземпляра модели Habit
        """

        self.habit = Habit.objects.get(pk=habit_pk) if habit_pk else None

        self.task = PeriodicTask.objects.filter(
            pk=self.habit.task).first() if habit_pk else None

        self.task_name = (
            f'task/{self.habit.name}/pk - {self.habit.pk}'
            f'/period - {self.habit.period}'
        ) if habit_pk else None

        self.data = {'telegram': self.habit.owner.telegram_chat,
                     "text": "Привет!\nПора потренировать привычку!\n"
                             f"Тебе нужно {self.habit.action} "
                             f"в {self.habit.place} "
                             f"за {self.habit.lide_time} секунд.\n"
                             f"Поехали!"} if habit_pk else None

        self.now = datetime.utcnow()

        self.time = datetime.combine(
            self.now.date(),
            self.habit.start_time
        ) if habit_pk else None

        self.start_time = (
            self.time if self.habit.start_time > self.now.time()
            else self.time + timedelta(days=1)
        ) if habit_pk else None

        self.schedule, self.create = IntervalSchedule.objects.get_or_create(
            every=self.habit.period, period=IntervalSchedule.DAYS
        ) if habit_pk else (None, None)

    def create_periodic_task(self):
        """
        Метод получает экземпляр привычки и на основе его атрибутов создает
        периодическую задачу. Необходим habit_id.
        :return: None
        """
        if self.data['telegram'] is None:
            return "Не возможно создать задачу, не указан ник телеграм"
        task = PeriodicTask.objects.create(
            name=self.task_name,
            task='habit.tasks.task_send_telegram_message',
            interval=self.schedule,
            kwargs=json.dumps(self.data),
            start_time=self.start_time,
        )
        task.save()
        self.habit.task = task.pk
        self.habit.save()

    def update_periodic_task(self) -> None:
        """
        Метод обновляет модель периодической задачи
        :return:
        """

        self.task.name = self.task_name
        self.task.interval = self.schedule
        self.task.kwargs = json.dumps(self.data)
        self.task.start_time = self.start_time
        self.task.save()

    @staticmethod
    def delete_periodic_task(task_id: int) -> None:
        """
        Метод удаляет периодическую задачу.
        :param task_id: id экземпляра модели PeriodicTask
        :return: None
        """
        task = PeriodicTask.objects.filter(pk=task_id).first()
        task.delete()
