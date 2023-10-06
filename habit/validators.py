from rest_framework.validators import ValidationError
from django.utils.translation import gettext_lazy as _


class RewardValidator:
    """Валидатор для создания экземпляра вознаграждения"""

    def __int__(self, fields):
        self.fields = fields

    def __call__(self, value):
        reward = value.get('reward')
        nice = value.get('nice')
        is_nice = value.get('is_nice')
        if reward or nice:
            if is_nice:
                raise ValidationError(_('Для приятной привычки не может быть создано вознаграждение'))

            if reward and nice:
                raise ValidationError(_('Не может быть выбрано 2 вознаграждения одновременно'))

        elif not reward and not nice and not is_nice:
            raise ValidationError(_('Не выбрано вознаграждение, должна быть выбрана либо приятная привычка либо '
                                    'описано вознаграждение'))


class LideTimeValidator:
    """Валидатор поля времени выполнения сериализатора привычки"""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        time = value.get('lide_time')
        if time > 120:
            raise ValidationError(_('Время выполнения не может быть больше 120 секунд'))
