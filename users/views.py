
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from users.models import User, Verify
from users.serializers import UserSerializer, VerifySerializer, UserCreateSerializer
from users.services import send_verify


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_id=_('Регистрация пользователя'),
    operation_description=_("Запрос возвращает список привычек принадлежащих аутентифицированному пользователю."),
    tags=[_('Авторизация')]
))
class UserCreateAPIView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_id=_('Редактирование пользователя'),
    operation_description=_("Запрос позволяет редактировать аутентифицированного пользователя"),
    tags=[_('Авторизация')]
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_id=_('Редактирование пользователя(полная перезапись)'),
    operation_description=_("Данный метод редактирования крайне не рекомендован."
                            " Запрос позволяет редактировать аутентифицированного пользователя"),
    tags=[_('Авторизация')]
))
class UserUpdateAPIView(UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_id=_('Удаление авторизованного пользователя'),
    operation_description=_("Запрос удаляет авторизованного пользователя"),
    tags=[_('Авторизация')]
))
class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id=_('Получение информации о определенном пользователе'),
    operation_description=_("Запрос возвращает детальную информацию о пользователе"),
    tags=[_('Авторизация')]
))
class UserDetailAPIView(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_id=_('Проверка кода верификации'),
    operation_description=_("Запрос проверяет код верификации пользователя"),
    tags=[_('Авторизация')]
))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_id=_('Проверка кода верификации(полная перезапись)'),
    operation_description=_("Запрос проверяет код верификации пользователя"),
    tags=[_('Авторизация')]
))
class VerifyUpdateAPIView(UpdateAPIView):
    """
    Представление для верификации пользователя.
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
