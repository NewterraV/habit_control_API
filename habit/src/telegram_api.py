import requests
from config import settings
from users.tasks import task_multiple_update_periodic_task
from users.models import User


class TelegramAPI:
    """Класс для работы с API Telegram"""

    def __init__(self):
        self.token = settings.TELEGRAM_TOKEN

    def send_message(self, telegram, text):
        """
            Метод отправки телеграм уведомления.
            :param telegram: ID телеграм чата
            :param text: сообщение
            :return: код ответа
            """

        url = (f'https://api.telegram.org/bot{self.token}/'
               f'sendMessage')
        params = {
            "chat_id": telegram,
            "text": text

        }

        response = requests.get(url=url, params=params)
        return response.status_code

    def get_chat_id(self):
        """
        Метод проверяет обновления и на их основе определяет ID чата
        телеграм конкретного пользователя
        :return:
        """
        url = (f'https://api.telegram.org/bot{self.token}/'
               f'getUpdates')
        params = {
            "allowed_updates": ['message']
        }

        response = requests.get(url=url, params=params).json()

        if response['ok'] is True:
            message_list = response['result']
        else:
            return "Нет новых обновлений"

        for obj in message_list:
            message = obj['message']
            if message['text'] != '/start':
                continue

            user = (User.objects.filter(telegram=message['chat']['username']).
                    first())
            if not user:
                continue

            if user.telegram_chat != message['chat']['id']:
                user.telegram_chat = message['chat']['id']
                user.save()
                task_multiple_update_periodic_task.delay(user_id=user.pk)

                self.send_message(
                    telegram=user.telegram_chat,
                    text='Регистрация чата успешно пройдена!')
        return 'Обновления получены'
