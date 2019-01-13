from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    is_activate = models.BooleanField(default=False)

    def __unicode__(self):

        return self.user.username
