from django.urls import path
from .views import (create_user, get_users,
                    login_user, delete_user, update_user,
                    renew_submission, make_submission, verify_user)

urlpatterns = [
    path('user/create_user', create_user, name='create_user'),
    path('get_users', get_users, name='get_users'),
    path('user/login_user', login_user, name='login_user'),
    path('user/delete_user/<str:username>', delete_user, name='delete_user'),
    path('user/update_user/<int:username>', update_user, name='update_user'),
    path('user/renew_submission/<str:username>', renew_submission, name='renew_submission'),
    path('user/make_submission', make_submission, name='make_submission'),
    path('user/verify_user/<str:username>', verify_user, name='verify_user'),
]