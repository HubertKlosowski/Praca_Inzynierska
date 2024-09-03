from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'usertype']
        extra_kwargs = {
            'password': {'write_only': True}  # nie zwracany w API
        }
