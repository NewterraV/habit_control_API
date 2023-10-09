from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, Verify


class GetUserMixin:
    """Миксин-класс для создания и авторизации пользователя"""

    def get_user(self) -> None:
        # Создание и авторизация пользователя
        user = User.objects.create(
            last_name='Иванов',
            first_name='Иван',
            email='test@test.com',
            is_active=True,
            telegram='vrsfesfsef',
        )
        user.save()
        user.set_password('qwer1234')
        user.save()

        auth_data = {
            "email": "test@test.com",
            "password": "qwer1234"
        }

        url = '/auth/token/'
        response = self.client.post(url, auth_data, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


class UserAPITestCase(GetUserMixin, APITestCase):

    def test_create(self):
        """Тест регистрации пользователя"""
        response = self.client.post(
            '/auth/user/create/',
            {
                'last_name': 'Иванов',
                'first_name': 'Иван',
                'email': 'vakin49282@locawin.com',
                'telegram': 'vrsfesfsef',
                "password": "qwer1234"
            },
            format='json'
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(Verify.objects.count(), 1)
        self.assertEquals(response.json(),
                          {
                              "pk": 1,
                              "first_name": "Иван",
                              "last_name": "Иванов",
                              "email": "vakin49282@locawin.com",
                              "telegram": "vrsfesfsef"
                          }
                          )

    def test_detail(self):
        """Тест предоставления детальной информации о пользователе"""
        self.get_user()
        response = self.client.get(
            '/auth/user/detail/1/'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(response.json(),
                          {
                              "pk": 1,
                              "first_name": "Иван",
                              "last_name": "Иванов",
                              "email": "test@test.com",
                              "telegram": "vrsfesfsef"
                          }
                          )

    def test_update(self):
        """Тест обновления пользователя"""
        self.get_user()
        response = self.client.put(
            '/auth/user/update/1/',
            {
                "first_name": "Иван",
                "last_name": "Абрамов",
                "email": "test@test.com",
                "telegram": "fgbnjrre"
            }

        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(response.json(),
                          {
                              "pk": 1,
                              "first_name": "Иван",
                              "last_name": "Абрамов",
                              "email": "test@test.com",
                              "telegram": "fgbnjrre"
                          }
                          )

    def test_delete(self):
        """Тест удаления пользователя"""
        self.get_user()
        self.assertEquals(User.objects.count(), 1)

        response = self.client.delete(
            '/auth/user/delete/1/'
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(User.objects.count(), 0)

    def test_verify(self):
        """Тест ввода кода верификации"""
        self.client.post(
            '/auth/user/create/',
            {
                'last_name': 'Иванов',
                'first_name': 'Иван',
                'email': 'vakin49282@locawin.com',
                'telegram': 'vrsfesfsef',
                "password": "qwer1234"
            },
            format='json'
        )

        self.assertEquals(Verify.objects.count(), 1)
        verify = Verify.objects.all().first()

        response = self.client.put(
            f'/auth/verify/{verify.pk}/',
            {
                'user_code': verify.verify_code
            }

        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Verify.objects.count(), 0)

        # Проверка валидатора
        self.client.post(
            '/auth/user/create/',
            {
                'last_name': 'Иванов',
                'first_name': 'Иван',
                'email': 'test@test.com',
                'telegram': 'vrsfesfsef',
                "password": "qwer1234"
            },
            format='json'
        )
        verify = Verify.objects.all().first()
        response = self.client.put(
            f'/auth/verify/{verify.pk}/',
            {
                'user_code': 0000
            }

        )
        print(response.json())
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.json(), {'non_field_errors': ['Количество символов должно быть равно 5-ти']})
