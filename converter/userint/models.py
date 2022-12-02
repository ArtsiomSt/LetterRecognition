from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount_of_operations = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)


class PictureForRecongition(models.Model):
    made_by_user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    picture_file = models.ImageField(upload_to='photos/%Y/%m/%d')
    recognised_text = models.TextField(blank=True, null=True, default='')
    proccesed = models.BooleanField(default=False)