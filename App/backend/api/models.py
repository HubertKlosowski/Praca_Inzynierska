from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100)
    usertype = models.IntegerField(default=0)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    submission_num = models.IntegerField(default=10, null=False)
    last_submission = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)

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
    LANGUAGE_CHOICES = [
        ('en', 'english'),
        ('pl', 'polish')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=10)
    time_taken = models.FloatField(default=0)
    llm_model = models.CharField(max_length=20, choices=LLM_CHOICES)
    # file = models.FileField(upload_to='submission_files/', null=True, blank=True)
    # entry = models.TextField(null=True, blank=True)

    def __str__(self):
        return (f'Submission info\n User:{self.user.username}, '
                f'Time (s): {self.time_taken}, Model: {self.llm_model}')