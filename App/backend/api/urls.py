from django.urls import path
from .views import (get_user, create_user, get_users,
                    login_user, delete_user, update_user,
                    renew_submission, send_file, get_answer,
                    save_chat, verify_user)

urlpatterns = [
    path('user/get_user', get_user, name='get_user'),
    path('user/create_user', create_user, name='create_user'),
    path('user/get_users', get_users, name='get_users'),
    path('user/login_user', login_user, name='login_user'),
    path('user/delete_user/<str:username>', delete_user, name='delete_user'),
    path('user/update_user/<int:user_id>', update_user, name='update_user'),
    path('user/renew_submission/<str:username>', renew_submission, name='renew_submission'),
    path('user/send_file', send_file, name='send_file'),
    path('user/get_answer', get_answer, name='get_answer'),
    path('user/save_chat', save_chat, name='save_chat'),
    path('user/verify_user/<str:username>', verify_user, name='verify_user'),
]