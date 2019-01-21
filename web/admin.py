from django.contrib import admin

# Register your models here.
from web.models import UserProfile, Card, Verification, Order

admin.site.register(UserProfile)
admin.site.register(Card)
admin.site.register(Verification)
admin.site.register(Order)
