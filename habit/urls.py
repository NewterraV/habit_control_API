from django.urls import path
from rest_framework.routers import DefaultRouter
from habit.apps import HabitConfig
from habit.views import HabitViewSet, HabitListAPIView, HabitDetailView

app_name = HabitConfig.name
router = DefaultRouter()
router.register('habits', HabitViewSet, basename='habits')


urlpatterns = [
    path('habits/publish/', HabitListAPIView.as_view(), name='habits_publish'),
    path('habits/publish/<int:pk>/', HabitDetailView.as_view(), name='habits_detail_publish')
] + router.urls
