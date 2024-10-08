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


class SubmissionFile(models.Model):
    LLM_CHOICES = [
        ('bert-base', 'BERT Base'),
        ('bert-large', 'BERT Large'),
        ('roberta-base', 'Roberta Base'),
        ('roberta-large', 'Roberta Large'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)
    llm_model = models.CharField(max_length=20, choices=LLM_CHOICES)
    file = models.FileField(upload_to='submission_files/')

    def __str__(self):
        return (f'Submission info\n User:{self.user.username}, '
                f'Sent: {self.sent_at}, Model: {self.llm_model}')


class SubmissionChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.JSONField(default=list)
