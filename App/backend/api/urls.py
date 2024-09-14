from django.urls import path
from .views import get_user, create_user, get_users, login, delete_user, update_user, renew_submission, SendFileView

urlpatterns = [
    path('user/get_user', get_user, name='get_user'),
    path('user/create_user', create_user, name='create_user'),
    path('user/get_users', get_users, name='get_users'),
    path('user/login', login, name='login'),
    path('user/delete_user/<str:username>', delete_user, name='delete_user'),
    path('user/update_user/<int:user_id>', update_user, name='update_user'),
    path('user/renew_submission/<str:username>', renew_submission, name='renew_submission'),
    path('user/send_file', SendFileView.as_view(), name='send_file'),
]