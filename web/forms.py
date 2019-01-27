from django import forms
from django.contrib.auth.models import User

from web.models import UserProfile, Card, Verification, Order, Message
from web.models import sourcecurrency


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=30, required=False, widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput())
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number',)
        exclude = ("card_holder",)


class cardForm(forms.ModelForm):
    class Meta:
        model = Card
        widgets = {'date_exp': forms.DateInput(attrs={'type': 'date'})}
        fields = ('card_number', 'date_exp', 'cvv', 'card_front', 'card_back')


class VerificationForm(forms.ModelForm):
    class Meta:
        model = Verification
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'})}
        fields = ('passport_code', 'country_name', 'birth_date', 'address', 'passport_photo')


class OrderForm(forms.ModelForm):
    source_currency = forms.ChoiceField(choices=sourcecurrency)
    destination_currency = forms.ChoiceField()
    card_number = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        membercards = kwargs.pop('cards')
        coins = kwargs.pop('coins')
        super(OrderForm, self).__init__(*args, **kwargs)
        mychoice = Card.objects.filter(card_holder=membercards, is_verified=True)
        choice = []
        for i in mychoice:
            choice.append((i.card_number, i.card_number))
        self.fields['card_number'] = forms.ChoiceField(choices=choice)
        self.fields['destination_currency'] = forms.ChoiceField(choices=coins)
        super(OrderForm, self).full_clean()

    class Meta:
        model = Order
        fields = ('source_currency', 'source_amount', 'destination_currency', 'destination_amount', 'receipt_code',
                  'blockchain_wallet', 'card_number')


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=60)
    phone_number = forms.CharField(max_length=15)


class MsgBoxForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'referrer', 'message')
