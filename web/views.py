import json
import sys

from django.contrib import messages

from web.forms import UserForm, UserProfileForm, cardForm

from web.forms import SignUpForm, UserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views import generic
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
    card_form = cardForm()
    card_form.fields['card_number'].widget.attrs.update({'placeholder': 'CardNumber'})
    card_form.fields['date_exp'].widget.attrs.update({'placeholder': 'Date Of EXP'})
    card_form.fields['cvv'].widget.attrs.update({'placeholder': 'CVV'})
    card_form.fields['card_front'].widget.attrs.update({'placeholder': 'Card Front Side'})
    card_form.fields['card_back'].widget.attrs.update({'placeholder': 'Card Back Side'})
    response = {"title": "Dashboard", "coins": {}, "dollar": {}, "card_form": card_form}
    return render(request, "panel/dashboard.html", context=response)


def law_page(request):
    return render(request, "law.html")


@csrf_exempt
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/accounts/dashboard/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('login.html', {}, context)


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
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
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
            return redirect('/accounts/profile/')
        else:
            return HttpResponse("<script> alert(\"{} {}\");</script>".format(user_form.errors, profile_form.errors))
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        user_form.fields['first_name'].widget.attrs.update({'placeholder': 'FirstName'})
        user_form.fields['last_name'].widget.attrs.update({'placeholder': 'LastName'})
        user_form.fields['username'].widget.attrs.update({'placeholder': 'UserName'})
        profile_form.fields['phone_number'].widget.attrs.update({'placeholder': 'PhoneNumber Ex: +98xxxxxxx'})
        user_form.fields['email'].widget.attrs.update({'placeholder': 'Email Ex: example@gmail.com'})
        user_form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        return render_to_response('signup.html',
                                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
                                  context)


@csrf_exempt
@login_required
def add_card(request):
    context = RequestContext(request)
    if request.method == 'POST':
        card_form = cardForm(request.POST, request.FILES)
        if card_form.is_valid():
            # card_form.initial = {"card_holder": request.user}
            # card_form.card_holder=request.user

            instance = card_form.save()
            instance.card_holder = request.user
            instance.save()
            messages.add_message(request,messages.SUCCESS,"Your Card Added Successfully")
            return redirect("/accounts/dashboard/")
        else:
            messages.add_message(request, messages.ERROR, card_form.errors)
            return redirect("/accounts/dashboard/")
    else:
        messages.add_message(request, messages.ERROR, 'You Should USE POST METHOD IN REQUEST')
        return redirect("/accounts/dashboard/")
