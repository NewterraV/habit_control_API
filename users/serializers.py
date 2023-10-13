from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from users.models import User, Verify
from users.tasks import task_send_verify
from users.validators import VerifyValidator


class UserSerializer(serializers.ModelSerializer):
    """Основной сериализатор для вывода информации о пользователях"""

    class Meta:
        model = User
        fields = 'pk', 'first_name', 'last_name', 'email', 'telegram',


class UserCreateSerializer(serializers.ModelSerializer):
    """Основной сериализатор для вывода информации о пользователях"""

    password = serializers.CharField(write_only=True, label=_('password'))

    def create(self, validated_data):
        """Переопределение для создания нового пользователя"""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        # Создаем код верификации
        verify = Verify.objects.create(user=user)
        verify.save()
        # Отправляем код верификации
        task_send_verify.delay(verify.pk)

        return user

    class Meta:
        model = User
        fields = 'pk', 'first_name', 'last_name', 'email', 'password', 'telegram',


class VerifySerializer(serializers.ModelSerializer):
    """Основной сериализатор для вывода кода верификации"""

    def get_validators(self):
        return [VerifyValidator(field=['user_code'], pk=self.context)]

    class Meta:
        model = Verify
        fields = 'user_code',
