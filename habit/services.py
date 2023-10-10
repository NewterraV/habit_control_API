
def send_telegram_message(telegram, place, action, lide_time):
    """
        Метод отправки телеграм уведомления.
        :param telegram: id телеграм пользователя
        :param place: место выполнения задачи
        :param action: действие
        :param lide_time: время за которое необходимо выполнить задачу
        :return: None
        """
    print(f'Я выполнилась{telegram} {place} {action} {lide_time}')
