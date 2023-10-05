from django.urls import path
from rest_framework.routers import DefaultRouter
from habit.apps import HabitConfig
from habit.views import HabitViewSet

app_name = HabitConfig.name
router = DefaultRouter()
router.register('habits', HabitViewSet, basename='habits')


urlpatterns = [

] + router.urls
