from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _


class VerifyValidator:
    """
    Валидатор верификации
    """

    def __init__(self, field, pk):
        self.field = field
        self.obj = pk

    def __call__(self, value):
        user_code = value.get('user_code')

        if len(str(user_code)) != 5:
            raise ValidationError(_('Количество символов должно быть '
                                    'равно 5-ти'))

        if user_code != self.obj.verify_code:
            raise ValidationError(_('Неверный код верификации'))
