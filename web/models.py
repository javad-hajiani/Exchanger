from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "User : " + self.user.username


class Card(models.Model):
    card_number = models.CharField(max_length=24)
    card_holder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_exp = models.DateField()
    cvv = models.CharField(max_length=10)
    card_front = models.ImageField(upload_to='cards/')
    card_back = models.ImageField(upload_to='cards/')

    def __unicode__(self):
        return self.card_holder.user.username

    def __str__(self):
        return "Card Number : {} for User : {}".format(self.card_number, self.card_holder)


class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    passport_code = models.CharField(max_length=30)
    country_name = models.CharField(max_length=20)
    birth_date = models.DateField()
    address = models.TextField(max_length=500)
    passport_photo = models.ImageField(upload_to='passport_photo/')
    is_verified = models.BooleanField(max_length=1, default=False)
    def __unicode__(self):
        return self.user.user

    def __str__(self):
        return "Verification for : {}".format(self.user)
