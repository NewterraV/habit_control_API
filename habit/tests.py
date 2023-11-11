from unittest.mock import ANY

from rest_framework import status
from rest_framework.test import APITestCase
from django_celery_beat.models import PeriodicTask

from habit.models import Habit, Reward, Nice
from users.tests import GetUserMixin
from habit.src.periodic_tusks import HabitPeriodicTask


class GetHabitMixin:

    def create_habit(self):
        response = self.client.post(
            '/habits/',
            {"name": "Привычка", "place": "Место действия",
             "action": "Действие", "start_time": "13:56:00",
             "lide_time": 100,
             "period": 1, "is_publish": True,
             "reward": {"is_nice": False,
                        "reward": "Описание вознаграждения", }},
            format='json'
        )
        return response

    def update_habit(self, id_habit):
        response = self.client.put(
            f'/habits/{id_habit}/',
            {"name": "Привычка обновлена", "place": "Место действия",
             "action": "Действие", "start_time": "13:56:00",
             "lide_time": 10, "period": 2, "is_publish": True,
             "reward": {"is_nice": False,
                        "reward": "Описание вознаграждения", }},
            format='json'
        )
        return response


class HabitAPITestCase(GetUserMixin, GetHabitMixin, APITestCase):
    """Testcase для представлений привычки"""

    def setUp(self):
        self.user = self.get_user()

    def test_create(self):
        """
        Тест функционала создания новой привычки, а так-же
        сопутствующих функций.
        :return: None
        """

        # Проверка создания обычной привычки
        response = self.create_habit()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED),
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Reward.objects.count(), 1)
        self.assertEqual(response.json(),
                         {"id": ANY, "name": "Привычка",
                          "place": "Место действия", "action": "Действие",
                          "start_time": "13:56:00", "lide_time": 100,
                          "period": 1, "is_publish": True,
                          "owner": self.user.pk,
                          "reward": {"is_nice": False, "nice": None,
                                     "reward": "Описание вознаграждения",
                                     "habit": ANY, }}
                         )

    def test_validation(self):
        """Тест валидации привычки"""
        nise = self.client.post(
            '/habits/',
            {"name": "Привычка", "place": "Место действия",
             "action": "Действие", "start_time": "13:56:00",
             "lide_time": 120, "period": 1, "is_publish": True,
             "reward": {"is_nice": True, }},
            format='json'
        )
        id_nice = nise.json()['id']
        nice = Nice.objects.filter(habit=id_nice).first()
        response = self.client.post(
            '/habits/',
            {"name": "Привычка", "place": "Место действия",
             "action": "Действие", "start_time": "13:56:00",
             "lide_time": 200, "period": 0, "is_publish": True,
             "reward": {"is_nice": False,
                        "reward": "Описание вознаграждения", }},
            format='json'
        )
        self.assertEqual(response.json(), {
            "non_field_errors": [
                "Время выполнения не может быть больше 120 секунд",
                "Период может быть числом от 1 до 7"
            ]
        })

        #     Тест валидации признака приятной привычки
        response = self.client.post(
            '/habits/',
            {"name": "Привычка", "place": "Место действия",
             "action": "Действие", "start_time": "13:56:00",
             "lide_time": 120, "period": 0, "is_publish": True,
             "reward": {"is_nice": True, "reward": "Описание вознаграждения",
                        "nice": nice.pk}},
            format='json'
        )
        self.assertEqual(response.json(), {
            "reward": {
                "non_field_errors": [
                    "Для приятной привычки не может быть создано "
                    "вознаграждение"
                ]
            }
        })

    def test_update(self):
        """Тест обновления привычки и сопутствующих функций"""
        habit = self.create_habit()

        # Проверка обновления основной информации о привычке
        response = self.update_habit(habit.json()['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {"id": ANY, "name": "Привычка обновлена",
                          "place": "Место действия", "action": "Действие",
                          "start_time": "13:56:00", "lide_time": 10,
                          "period": 2, "is_publish": True,
                          "owner": self.user.pk,
                          "reward": {"is_nice": False, "nice": None,
                                     "reward": "Описание вознаграждения",
                                     "habit": ANY, }})

        # Проверка изменения привычки с полезной на приятную
        response = self.client.put(
            f'/habits/{habit.json()["id"]}/',
            {"name": "Привычка стала приятной", "place": "Место действия",
             "action": "Действие",
             "start_time": "13:56:00", "lide_time": 10, "period": 2,
             "is_publish": True,
             "reward": {"is_nice": True, }},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f'/habits/{habit.json()["id"]}/')
        self.assertEqual(response.json(),
                         {"id": ANY, "name": "Привычка стала приятной",
                          "place": "Место действия",
                          "action": "Действие", "start_time": "13:56:00",
                          "lide_time": 10, "period": 2,
                          "is_publish": True, "owner": ANY,
                          "reward": {"is_nice": True, "nice": None,
                                     "reward": None, "habit": ANY, }})

    def test_list(self):
        """
        Тест вывода списка привычек пользователя.
        :return:
        """
        self.create_habit()
        self.create_habit()
        self.create_habit()
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'count': 3, 'next': None, 'previous': None,
                          'results': [
                              {'id': ANY, 'name': 'Привычка',
                               'place': 'Место действия',
                               'action': 'Действие', 'start_time': '13:56:00',
                               'lide_time': 100, 'period': 1,
                               'is_publish': True, 'owner': self.user.pk,
                               'reward': {'is_nice': False, 'nice': None,
                                          'reward': 'Описание вознаграждения',
                                          'habit': ANY}},
                              {'id': ANY, 'name': 'Привычка',
                               'place': 'Место действия',
                               'action': 'Действие', 'start_time': '13:56:00',
                               'lide_time': 100, 'period': 1,
                               'is_publish': True, 'owner': self.user.pk,
                               'reward': {'is_nice': False, 'nice': None,
                                          'reward': 'Описание вознаграждения',
                                          'habit': ANY}},
                              {'id': ANY, 'name': 'Привычка',
                               'place': 'Место действия',
                               'action': 'Действие', 'start_time': '13:56:00',
                               'lide_time': 100, 'period': 1,
                               'is_publish': True, 'owner': self.user.pk,
                               'reward': {'is_nice': False, 'nice': None,
                                          'reward': 'Описание вознаграждения',
                                          'habit': ANY}}]}
                         )

    def test_detail(self):
        """Тест получения детальной информации о привычке"""
        self.client.post(
            '/habits/',
            {"name": "Привычка приятная", "place": "Место действия",
             "action": "Действие", "start_time": "13:56:00",
             "lide_time": 100,
             "period": 1, "is_publish": True,
             "reward": {"is_nice": True}},
            format='json'
        )
        id_nice = Nice.objects.get().pk
        habit = self.client.post(
            '/habits/',
            {"name": "Привычка", "place": "Место действия",
             "action": "Действие", "start_time": "13:56:00",
             "lide_time": 100,
             "period": 1, "is_publish": True,
             "reward": {"is_nice": False, "nice": id_nice, }},
            format='json'
        )
        response = self.client.get(
            f'/habits/{habit.json()["id"]}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': ANY, 'name': 'Привычка',
                          'place': 'Место действия', 'action': 'Действие',
                          'start_time': '13:56:00', 'lide_time': 100,
                          'period': 1, 'is_publish': True,
                          'owner': self.user.pk,
                          'reward': {'is_nice': False, 'nice': ANY,
                                     'reward': None, 'habit': ANY,
                                     'nice_detail':
                                         {'name': 'Привычка приятная',
                                          'place': 'Место действия',
                                          'action': 'Действие',
                                          'start_time': '13:56:00',
                                          'lide_time': 100}}}

                         )

    def test_publish(self):
        """Тест вывода опубликованных привычек"""

        self.create_habit()
        self.create_habit()
        not_publish = self.client.post(
            '/habits/',
            {"name": "Привычка", "place": "Место действия",
             "action": "Действие", "start_time": "13:56:00",
             "lide_time": 100,
             "period": 1, "is_publish": False,
             "reward": {"is_nice": False, "reward": "Описание вознаграждения"}
             },
            format='json'
        )
        response = self.client.get('/habits/publish/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)

        response = self.client.get(
            f'/habits/publish/{not_publish.json()["id"]}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(
            f'/habits/publish/{str(int(not_publish.json()["id"]) - 1)}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_work_periodic_task(self):
        """Тест работы с периодическими задачами на основе привычек"""
        # Проверка создания периодической задачи
        habit = self.create_habit()
        habit_task = HabitPeriodicTask(habit_pk=habit.json()['id'])
        habit_task.create_periodic_task()
        self.assertEqual(PeriodicTask.objects.count(), 1)

        # Проверка обновления периодической задачи
        self.update_habit(habit.json()['id'])
        habit_task = HabitPeriodicTask(habit_pk=habit.json()['id'])
        habit_task.update_periodic_task()
        task = PeriodicTask.objects.get(pk=habit_task.habit.task)
        self.assertEqual(
            task.name,
            f'task/Привычка обновлена/pk - {habit.json()["id"]}/period - 2')

        # Проверка удаления периодической задачи
        habit_task = HabitPeriodicTask(habit_pk=habit.json()['id'])
        habit_task.delete_periodic_task(task_id=habit_task.habit.task)
        self.assertEqual(PeriodicTask.objects.count(), 0)
