from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import Verify


class VerifyValidator:
    """
    Валидатор верификации
    """

    def __init__(self, field, pk):
        self.field = field
        self.obj = pk

    def __call__(self, value):
        user_code = value.get('user_code')
        if user_code != self.obj.verify_code:
            raise ValidationError(_('Неверный код верификации'))
