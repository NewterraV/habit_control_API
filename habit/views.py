from rest_framework import viewsets
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from habit.models import Habit
from habit.paginators import HabitsPagination
from habit.serializers import HabitSerializer
from drf_yasg.utils import swagger_auto_schema

from habit.tasks import task_create_periodic_task, task_delete_periodic_task, task_update_periodic_task


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_id=_('Получение списка привычек пользователя'),
    operation_description=_("Запрос возвращает список привычек принадлежащих аутентифицированному пользователю."),
    tags=[_('Привычки')]
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_id=_('Создание привычки'),
    operation_description=_("Данный запрос создает новую привычку. При создании так-же инициализируется создание "
                            "записей в связанных моделях. Обратите внимание, что привычка имеет флаг  is_nice. "
                            "Если во флаге передано значение true, то данная привычка считается приятной "
                            "и в неё не может быть передано вознаграждение. "
                            "При принудительной передаче возникнет ошибка валидации. Если же стоит флаг false, то "
                            "привычка считается полезной и для неё необходима передача вознаграждения, которое будет "
                            "либо ссылкой на приятную привычку, либо обычным описанием вознаграждения. Эти параметры "
                            "взаимоисключающие, если передать 2 одновременно - возникнет ошибка валидации."),
    tags=[_('Привычки')]
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_id=_('Редактирование привычки'),
    operation_description=_("Данный запрос позволяет пользователю редактировать привычку."
                            "При этом возможно изменение привычки с полезной на приятную и наоборот. "
                            "Валидация та же что и в запросе создания привычки."),
    tags=[_('Привычки')]
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_id=_('Перезапись привычки'),
    operation_description=_("Данный запрос позволяет пользователю редактировать привычку."
                            "При этом возможно изменение привычки с полезной на приятную и наоборот. "
                            "Валидация та же что и в запросе создания привычки."),
    tags=[_('Привычки')]
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_id=_('Получение информации о привычке'),
    operation_description=_("Данный запрос выводит информацию об отдельной привычке принадлежащей авторизованному"
                            " пользователю"),
    tags=[_('Привычки')]
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_id=_('Удаление привычки'),
    operation_description=_("Данный запрос удаляет привычку и все данные связанные с ней. Если привычка приятная то во"
                            " всех привычках которые используют удаляемую привычку в качестве награды устанавливается"
                            " нулевое значение"),
    tags=[_('Привычки')]
))
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    default_serializers = HabitSerializer
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination

    def perform_create(self, serializer):
        """Переопределение метода для автоматической установки владельца и создания периодической задачи"""
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()
        task_create_periodic_task.delay(habit.pk)

    def perform_update(self, serializer):
        """Переопределение для обновления периодической задачи при обновлении привычки"""
        habit = serializer.save()
        task_update_periodic_task.delay(habit.pk)

    def perform_destroy(self, instance):
        """Переопределение для удаления периодической задачи при удалении привычки"""
        task_delete_periodic_task.delay(instance.task)
        instance.delete()


@method_decorator(name='get', decorator=swagger_auto_schema(
        operation_id=_('Получение списка общедоступных привычек'),
        operation_description=_("Данный запрос выводит список общедоступных привычек (флаг is_publish)"),
        tags=[_('Привычки')],
    ))
class HabitListAPIView(generics.ListAPIView):

    swagger_auto_schema(
        operation_id=_('Получение списка общедоступных привычек'),
        operation_description=_("Данный запрос выводит список общедоступных привычек (флаг is_publish)"),
        tags=[_('Привычки')],
    )

    queryset = Habit.objects.filter(is_publish=True)
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination


@method_decorator(name='get', decorator=swagger_auto_schema(
        operation_id=_('Получение информации о общедоступной привычке'),
        operation_description=_("Данный запрос выводит информацию о общедоступной привычке (флаг is_publish)"),
        tags=[_('Привычки')],
    ))
class HabitDetailView(generics.RetrieveAPIView):
    queryset = Habit.objects.filter(is_publish=True)
    serializer_class = HabitSerializer
