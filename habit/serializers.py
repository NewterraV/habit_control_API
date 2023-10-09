from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from habit.models import Habit, Reward, Nice
from habit.validators import RewardValidator, LideTimeValidator


class HabitReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = 'name', 'place', 'action', 'start_time', 'lide_time'


class RewardSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели Reward
    """

    validators = [
        RewardValidator()
    ]

    nice_detail = HabitReadSerializer(source='nice.habit', read_only=True, label=_('data about a pleasant habit'))

    class Meta:
        model = Reward
        fields = 'is_nice', 'nice', 'reward', 'habit', 'nice_detail'


class HabitSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для вывода модели привычек
    """

    reward = RewardSerializer(label=_('rewards'))

    validators = [
        LideTimeValidator(fields='lide_time')
    ]

    class Meta:
        model = Habit
        fields = '__all__'

    def create(self, validated_data):
        """Переопределение для создания привычки"""

        reward_data = validated_data.pop('reward')
        habit = Habit.objects.create(**validated_data)
        habit.save()
        reward = Reward.objects.create(**reward_data, habit=habit)
        reward.save()
        if reward.is_nice:
            nice = Nice.objects.create(habit=habit)
            nice.save()
            return habit
        return habit

    def update(self, instance, validated_data):
        """Переопределение для обновления привычки"""

        # Извлекаем данные из информации прошедшей валидацию и получаем объект
        reward_data = validated_data.pop('reward')

        # получаем объект модели Reward
        Reward.objects.filter(id=instance.reward.pk).update(**reward_data)
        reward = Reward.objects.filter(id=instance.reward.pk).first()

        # Может быть, что пользователь изменит привычку с полезной на приятную или наоборот.
        # Логика ниже обрабатывает данное изменение
        if not reward.is_nice and Nice.objects.filter(habit=instance.pk):
            Nice.objects.filter(habit=instance.pk).delete()
            return super().update(instance, validated_data)
        if reward.is_nice:
            nice = Nice.objects.filter(habit=instance.pk)
            reward.reward = None
            reward.nice = None
            reward.save()
            if nice:
                return super().update(instance, validated_data)
            new_nice = Nice.objects.create(habit=instance)
            new_nice.save()
        return super().update(instance, validated_data)
