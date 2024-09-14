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

    def __str__(self):
        return (f'User info\n name: {self.name}, email: {self.email}, '
                f'username: {self.username}, usertype: {self.usertype}, '
                f'created_at: {self.created_at}, submission_num: {self.submission_num}')


class Submission(models.Model):
    LLM_CHOICES = [
        ('bert-base', 'BERT Base'),
        ('bert-large', 'BERT Large'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)
    llm_model = models.CharField(max_length=20, choices=LLM_CHOICES)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return f'{self.user.username} - {self.sent_at} - {self.llm_model}'