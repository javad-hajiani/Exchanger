from django.contrib import messages
from django.db import IntegrityError
from web.forms import UserProfileForm, cardForm, VerificationForm
from web.forms import UserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
import requests


@csrf_exempt
def redirect_view(request):
    response = redirect("/{}/".format("home"))
    return response


@csrf_exempt
def home_page(request):
    response = {"title": "Exchanger", "coins": getcoins(), "dollar": getdollar()}
    return render(request, "home.html", context=response)


def getcoins():
    coin = requests.get("https://chasing-coins.com/api/v1/top-coins/20").json()
    return coin


def getdollar():
    dollar = requests.post('https://payment24.ir/api/product/currency-price-calculation?product=cards_buy',
                           '{"product": "cards_buy"}').json()
    return dollar["data"]["currencies"]["USD"]


@csrf_exempt
def aboutus_page(request):
    response = {"title": "AboutUs"}
    return render(request, "aboutus.html", context=response)


@csrf_exempt
def contactus_page(request):
    response = {"title": "Contact Us"}
    return render(request, "contactus.html", context=response)


@csrf_exempt
@login_required
def dashboard_page(request):
    ######################## Card Form Place Holders ################
    card_form = cardForm()
    card_form.fields['card_number'].widget.attrs.update({'placeholder': 'CardNumber'})
    card_form.fields['date_exp'].widget.attrs.update({'placeholder': 'Date Of EXP'})
    card_form.fields['cvv'].widget.attrs.update({'placeholder': 'CVV'})
    card_form.fields['card_front'].widget.attrs.update({'placeholder': 'Card Front Side'})
    card_form.fields['card_back'].widget.attrs.update({'placeholder': 'Card Back Side'})
    ######################## Verification Form Place Holders ################
    verification_form = VerificationForm()
    verification_form.fields['passport_code'].widget.attrs.update({'placeholder': 'Passport Code'})
    verification_form.fields['country_name'].widget.attrs.update({'placeholder': 'Country Name'})
    verification_form.fields['birth_date'].widget.attrs.update({'placeholder': 'Date of Birth'})
    verification_form.fields['address'].widget.attrs.update({'placeholder': 'Address'})
    verification_form.fields['passport_photo'].widget.attrs.update({'placeholder': 'Passport Photo'})
    ######################## End ################
    response = {"title": "Dashboard", "coins": {}, "dollar": {}, "card_form": card_form,
                "Verification_Form": verification_form}
    return render(request, "panel/dashboard.html", context=response)


def law_page(request):
    return render(request, "law.html")


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "You're Logged in Successfully")
                return redirect('/accounts/dashboard/')
            else:
                messages.add_message(request, messages.ERROR, "Your account is disabled.")
                return redirect("/home/")
        else:
            messages.add_message(request, messages.ERROR, "Invalid login details supplied.")
            return redirect("/home")
    else:
        return render('login.html', context={})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/home/")


@login_required
@csrf_exempt
def profile_page(request):
    return render(request, "panel/profile.html", context={})


@csrf_exempt
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True  # Invalid form or forms - mistakes or something else?
                username = user_form.cleaned_data.get('username')
                raw_password = user_form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
            return redirect('/accounts/profile/')
        else:
            messages.add_message(request, messages.ERROR, user_form.errors + ' ' + profile_form.errors)
            redirect('/home/')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        user_form.fields['first_name'].widget.attrs.update({'placeholder': 'FirstName'})
        user_form.fields['last_name'].widget.attrs.update({'placeholder': 'LastName'})
        user_form.fields['username'].widget.attrs.update({'placeholder': 'UserName'})
        profile_form.fields['phone_number'].widget.attrs.update({'placeholder': 'PhoneNumber Ex: +98xxxxxxx'})
        user_form.fields['email'].widget.attrs.update({'placeholder': 'Email Ex: example@gmail.com'})
        user_form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        return render('signup.html',
                      context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


@csrf_exempt
@login_required
def add_card(request):
    if request.method == 'POST':
        card_form = cardForm(request.POST, request.FILES)
        if card_form.is_valid():
            try:
                instance = card_form.save()
                instance.card_holder = request.user
                instance.save()
                messages.add_message(request, messages.SUCCESS, "Your Card Added Successfully")
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
            return redirect("/accounts/dashboard/")
        else:
            messages.add_message(request, messages.ERROR, card_form.errors)
            return redirect("/accounts/dashboard/")
    else:
        messages.add_message(request, messages.ERROR, 'You Should USE POST METHOD IN REQUEST')
        return redirect("/accounts/dashboard/")


@login_required
@csrf_exempt
def verification_page(request):
    if request.method == 'POST':
        verification_form = VerificationForm(request.POST, request.FILES)
        if verification_form.is_valid():
            try:
                instance = verification_form.save()
                instance.user = request.user
                instance.save()
                messages.add_message(request, messages.SUCCESS, "Your Verification Document Added Successfully")
            except IntegrityError:
                messages.add_message(request, messages.ERROR, 'Your User Already have Verification Request!')
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
            return redirect("/accounts/dashboard/")
        else:
            messages.add_message(request, messages.ERROR, verification_form.errors)
            return redirect("/accounts/dashboard/")
    else:
        messages.add_message(request, messages.ERROR, 'You Should USE POST METHOD IN REQUEST')
        return redirect("/accounts/dashboard/")
