from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def redirect_view(request):
    response = redirect("/{}/".format("home"))
    return response
@csrf_exempt
def home(request):
    body={"name":"test", "family":"test2"}
    response={"body": body, "title": "Exchanger"}
    return render(request,"home.html", context=response)