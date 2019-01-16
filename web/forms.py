from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from web.models import UserProfile, Card, Verification


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=30, required=False, widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput())
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'picture')
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
