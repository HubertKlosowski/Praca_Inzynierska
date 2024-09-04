from django.urls import path
from .views import get_user, create_user, get_users, login

urlpatterns = [
    path('user/get_user', get_user, name='get_user'),
    path('user/create_user', create_user, name='create_user'),
    path('user/get_users', get_users, name='get_users'),
    path('user/login', login, name='login'),
]