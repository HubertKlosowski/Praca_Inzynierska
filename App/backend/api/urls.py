from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (create_user, get_users,
                    LoginView, delete_user, update_user,
                    renew_submission, make_submission, verify_user,
                    get_submission, change_name, get_user_data)

urlpatterns = [
    path('user/create_user', create_user, name='create_user'),
    path('get_users', get_users, name='get_users'),
    path('user/delete_user', delete_user, name='delete_user'),
    path('user/update_user', update_user, name='update_user'),
    path('user/get_user_data', get_user_data, name='get_user_data'),
    path('user/renew_submission', renew_submission, name='renew_submission'),
    path('submission/make_submission', make_submission, name='make_submission'),
    path('submission/get_submission/<str:sub_uuid>', get_submission, name='get_submission'),
    path('user/verify_user', verify_user, name='verify_user'),
    path('submission/change_name/<str:sub_uuid>', change_name, name='change_name'),
    path('user/login_user', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]