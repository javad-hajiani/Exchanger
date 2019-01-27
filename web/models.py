from django.contrib.auth.models import User
from django.db import models

sourcecurrency = [('USD', 'USD'), ('IRR', 'IRR'), ('BTC', 'BTC')]
referrers = [('Friends', 'Friends'), ('Search Engine', 'Search Engine'), ('Advertisement', 'Advertisement'),
             ('Other', 'Other')]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=25, blank=True)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return "User : " + self.user.username


class Card(models.Model):
    card_number = models.CharField(max_length=80)
    card_holder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_exp = models.DateField()
    cvv = models.CharField(max_length=80)
    card_front = models.ImageField(upload_to='cards/')
    card_back = models.ImageField(upload_to='cards/')
    is_verified = models.BooleanField(default=False)
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
    is_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.user

    def __str__(self):
        return "Verification for : {}".format(self.user)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    source_currency = models.CharField(max_length=10, choices=sourcecurrency)
    source_amount = models.CharField(max_length=60)
    destination_currency = models.CharField(max_length=10)
    order_date = models.DateTimeField(auto_now=True)
    destination_amount = models.CharField(max_length=70)
    receipt_code = models.CharField(max_length=80)
    blockchain_wallet = models.CharField(max_length=80)
    card_number = models.CharField(max_length=80)
    status = [('Pending', 'Pending'), ('Success', 'Success')]
    transaction_status = models.CharField(default='Pending', max_length=10, choices=status)

    def __unicode__(self):
        return self.user.user

    def __str__(self):
        return "Order for {} from {} to {} is {}".format(self.user, self.source_currency, self.destination_currency,
                                                         self.transaction_status)


class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, max_length=50)
    referrer = models.CharField(choices=referrers, max_length=12)
    message = models.TextField(max_length=500)

    def __str__(self):
        return "{}  {}".format(self.name, self.email)
