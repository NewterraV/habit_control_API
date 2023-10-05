from django.shortcuts import render
from rest_framework import viewsets

from habit.models import Habit
from habit.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):

    queryset = Habit.objects.all()
    default_serializers = HabitSerializer
    serializer_class = HabitSerializer
