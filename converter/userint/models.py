from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount_of_operations = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)