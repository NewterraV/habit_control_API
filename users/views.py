from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from users.models import User, Verify
from users.serializers import UserSerializer, VerifySerializer
from users.services import send_verify


class UserCreateAPIView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Переопределение для создания кода верификации"""
        # Создаем пользователя
        password = self.request.data['password']
        new_user = serializer.save()
        new_user.set_password(password)
        new_user.save()
        # Создаем код верификации
        verify = Verify.objects.create(user=new_user)
        verify.save()
        # Отправляем код верификации
        send_verify(verify)


class UserUpdateAPIView(UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VerifyUpdateAPIView(UpdateAPIView):
    """
    Представление для
    """
    queryset = Verify.objects.all()
    serializer_class = VerifySerializer

    def update(self, request, *args, **kwargs):
        """
        Переопределение для передачи дополнительного контекста в сериализатор
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=partial, context=self.get_object())
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        """Переопределение для проверки кода верификации"""
        verify = serializer.save()
        user = verify.user
        user.is_active = True
        user.save()
        verify.delete()
