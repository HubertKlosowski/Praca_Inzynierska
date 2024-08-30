from django.urls import path
from .views import get_user_by_username, create_user, get_users, get_user_by_email

urlpatterns = [
    path('user/username/<str:username>', get_user_by_username, name='get_user_by_username'),
    path('user/create_user', create_user, name='create_user'),
    path('user/get_users', get_users, name='get_users'),
    path('user/email/<str:email>', get_user_by_email, name='get_user_by_email'),
]