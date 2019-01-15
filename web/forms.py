from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from web.models import UserProfile, Card


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=16, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'UserName '}),
            'password1': forms.TextInput(attrs={'placeholder': 'FirstName '})}


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=30,required=False,widget=forms.PasswordInput())
    first_name=forms.CharField(max_length=30,required=False,widget=forms.TextInput())
    last_name=forms.CharField(max_length=30,required=False,widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'is_verified', 'picture')
        exclude =("card_holder", )


class cardForm(forms.ModelForm):
    class Meta:
        model = Card
        widgets = {'date_exp': forms.DateInput(attrs={'type': 'date'})}
        fields = ('card_number','date_exp','cvv','card_front','card_back')