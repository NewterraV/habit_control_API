from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics

from habit.models import Habit
from habit.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):

    queryset = Habit.objects.all()
    default_serializers = HabitSerializer
    serializer_class = HabitSerializer


class HabitListAPIView(generics.ListAPIView):

    queryset = Habit.objects.filter(is_publish=True)
    serializer_class = HabitSerializer


class HabitDetailView(generics.RetrieveAPIView):

    queryset = Habit.objects.filter(is_publish=True)
    serializer_class = HabitSerializer
