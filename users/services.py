from typing import Any
from django.core.mail import send_mail
from django.conf import settings


def send_verify(obj: Any) -> None:
    """
    Метод отправляет на email нового пользователя код для активации аккаунта
    :param obj: Экземпляр модели Verify
    :return: None
    """
    send_mail(
        'Подтвердите ваш Email',
        f'Код верификации {obj.verify_code} \n Ссылка для ввода кода верификации: '
        f'http://127.0.0.1:8000/auth/verify/{obj.pk}',
        settings.EMAIL_HOST_USER,
        [obj.user.email]
    )
