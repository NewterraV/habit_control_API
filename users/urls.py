from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserUpdateAPIView, UserDeleteAPIView, UserDetailAPIView, VerifyUpdateAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/detail/<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('user/delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user_delete'),
    path('verify/<int:pk>/', VerifyUpdateAPIView.as_view(), name='verify'),
]
