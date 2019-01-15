from django.contrib import admin

# Register your models here.
from web.models import UserProfile, Card

admin.site.register(UserProfile)
admin.site.register(Card)