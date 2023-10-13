from typing import Any
from django.core.mail import send_mail
from django.conf import settings

from users.models import Verify


def send_verify(verify_pk: Any) -> int:
    """
    Метод отправляет на email нового пользователя код для активации аккаунта
    :param verify_pk: pk модели Verify
    :return: количество успешно отправленных писем
    """
    verify = Verify.objects.get(pk=verify_pk)

    status = send_mail(
        'Подтвердите ваш Email',
        f'Код верификации {verify.verify_code} \n Ссылка для ввода кода верификации: '
        f'http://127.0.0.1:8000/auth/verify/{verify.pk}',
        settings.EMAIL_HOST_USER,
        [verify.user.email]
    )
    return status
