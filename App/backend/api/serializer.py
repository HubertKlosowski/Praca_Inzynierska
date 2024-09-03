from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'