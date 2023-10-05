from rest_framework import serializers

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для вывода модели привычек
    """

    class Meta:
        model = Habit
        fields = '__all__'
