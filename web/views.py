import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import requests
@csrf_exempt
def redirect_view(request):
    response = redirect("/{}/".format("home"))
    return response
@csrf_exempt
def home(request):
    response={"n": range(1,20), "title": "Exchanger", "coins": getcoins() , "dollar" : getdollar() }
    return render(request,"home.html", context=response)


def getcoins():
    coin=requests.get("https://chasing-coins.com/api/v1/top-coins/20").json()
    return coin

def getdollar():
    dollar=requests.post('https://payment24.ir/api/product/currency-price-calculation?product=cards_buy','{"product": "cards_buy"}').json()
    return dollar["data"]["currencies"]["USD"]