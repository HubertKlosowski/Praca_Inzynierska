import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils import timezone


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    usertype = models.IntegerField(default=0)
    password = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)
    submission_num = models.IntegerField(default=10, null=False)
    last_submission = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['username', 'email', 'name', 'usertype']

    def __str__(self):
        return (f'User info\n name: {self.name}, email: {self.email}, '
                f'username: {self.username}, usertype: {self.usertype}, '
                f'created_at: {self.created_at}, submission_num: {self.submission_num}'
                f'last_submission: {self.last_submission}, is_verified: {self.is_verified}')


class Submission(models.Model):
    LLM_CHOICES = [
        ('bert-base', 'BERT Base'),
        ('bert-large', 'BERT Large'),
        ('roberta-base', 'Roberta Base'),
        ('roberta-large', 'Roberta Large'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    time_taken = models.FloatField(default=0)
    model = models.CharField(max_length=20, choices=LLM_CHOICES)
    content = models.FileField(upload_to='submission_files/', null=True, blank=True)

    def __str__(self):
        return (f'Submission info\n User:{self.user.username}, '
                f'Time (s): {self.time_taken}, Model: {self.model}')