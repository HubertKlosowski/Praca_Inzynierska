from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=255)
    usertype = models.IntegerField(default=0)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True)
    submission_num = models.IntegerField(default=10, null=False)

    def __str__(self):
        return (f'User info\n name: {self.name}, email: {self.email}, '
                f'username: {self.username}, usertype: {self.usertype}, '
                f'created_at: {self.created_at}, submission_num: {self.submission_num}')
