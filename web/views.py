import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
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
    response = {"title": "Dashboard"}
    return render(request, "dashboard.html", context=response)


@csrf_exempt
def signup_page(request):
    response = {"title": "SignUp Page"}
    return render(request, "signup.html", context=response)


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
