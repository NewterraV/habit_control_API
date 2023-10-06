from rest_framework import serializers

from habit.models import Habit, Reward, Nice
from habit.validators import RewardValidator, LideTimeValidator


class RewardSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели Reward
    """

    validators = [
        RewardValidator()
    ]

    class Meta:
        model = Reward
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для вывода модели привычек
    """

    reward = RewardSerializer()

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
