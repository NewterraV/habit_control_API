from celery import shared_task
from users.services import send_verify


@shared_task
def task_send_verify(verify_pk: int) -> None:
    """
    Отложенная задача отправляет письмо с кодом верификации
    :param verify_pk: ID модели верификации
    :return: None
    """
    send_verify(verify_pk)
