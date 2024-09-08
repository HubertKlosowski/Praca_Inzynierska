from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=255)
    usertype = models.IntegerField(default=0)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'User {self.name} {self.email} {self.username} {self.usertype} {self.created_at}'
