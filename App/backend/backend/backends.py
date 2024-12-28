from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from api.models import User


# służy do uwierzytelniania użytkownika
# wykorzystuje pole is_verified w modelu Usera (obejście property is_authenticated, która zwraca zawsze True)
class UserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.is_verified and check_password(password, user.password):
                return user
            else:
                return None
        else:
            return None

    def get_user(self, user_id):
        if User.objects.filter(id=user_id).exists():
            return User.objects.get(id=user_id)
        else:
            return None