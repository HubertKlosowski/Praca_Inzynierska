from rest_framework import serializers
from .models import User, SubmissionFile, SubmissionChat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = '__all__'

class SubmissionChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionChat
        fields = '__all__'
