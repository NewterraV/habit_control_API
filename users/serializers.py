from rest_framework import serializers

from users.models import User, Verify
from users.validators import VerifyValidator


class UserSerializer(serializers.ModelSerializer):
    """Основной сериализатор для вывода информации о пользователях"""

    class Meta:
        model = User
        fields = 'pk', 'first_name', 'last_name', 'email', 'telegram',


class VerifySerializer(serializers.ModelSerializer):
    """Основной сериализатор для вывода кода верификации"""

    def get_validators(self):
        print(self.context)
        return [VerifyValidator(field=['user_code'], pk=self.context)]

    class Meta:
        model = Verify
        fields = 'user_code',
