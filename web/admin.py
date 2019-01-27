from django.contrib import admin

from web.models import UserProfile, Card, Verification, Order, Message


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'source_currency', 'source_amount', 'destination_currency', 'destination_amount', 'order_date',
        'receipt_code', 'blockchain_wallet', 'card_number', 'transaction_status')


class VerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'passport_code', 'country_name', 'birth_date', 'address', 'is_verified')


class CardAdmin(admin.ModelAdmin):
    list_display = ("card_holder", 'card_number', 'date_exp', 'cvv', 'is_verified')
    Card.card_holder.empty_value_display = 'Not Available'


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Verification, VerificationAdmin)
admin.site.register(Order, OrderAdmin)

admin.site.register(Message)
