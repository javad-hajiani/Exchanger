import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django_function_cache import cached

from web.forms import UserForm, OrderForm, ProfileForm, MsgBoxForm
from web.forms import UserProfileForm, cardForm, VerificationForm
from web.models import Verification, Order, UserProfile


#
# def user_cards(request):
#     response = []
#     for i in orders:
#         response.append(i)
#     return HttpResponse(response)


def coinsselector():
    response = []
    response.append(('USD', 'USD'))
    response.append(('IRR', 'IRR'))
    coins = cached(getcoins)()
    for i in coins["data"]:
        if int(i["rank"]) <= 20:
            response.append((i["symbol"], i["symbol"]))
    return response


@csrf_exempt
def redirect_view(request):
    response = redirect("/{}/".format("home"))
    return response


@csrf_exempt
def home_page(request):
    messageform = MsgBoxForm()
    response = {"title": "Exchanger", "coins": cached(getcoins)(), "dollar": cached(getdollar)(),
                "MsgForm": messageform}
    return render(request, "home.html", context=response)



def getcoins():
    coin = requests.get("https://api.coincap.io/v2/assets").json()
    return coin
def getdollar():
    content = requests.get('https://bonbast.com').text
    soup = BeautifulSoup(content)
    dollar = int(soup.find_all(id='usd1')[0].text)
    return dollar


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
    verified = Verification.objects.filter(user=request.user).first()
    if verified:
        verified = verified.is_verified
    else:
        verified = False
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
    ######################## Order Form Place Holders ################
    order_form = OrderForm(cards=request.user, coins=coinsselector())
    order_form.fields['receipt_code'].widget.attrs.update({'id': 'nextstep123'})
    # order_form.fields['receipt_code'].widget.attrs.update({'style': 'display:none;'})
    order_form.fields['blockchain_wallet'].widget.attrs.update({'id': 'nextstep1234'})
    order_form.fields['source_amount'].widget.attrs.update({'onchange': 'setamount()'})
    order_form.fields['source_currency'].widget.attrs.update({'onchange': 'setamount()'})
    order_form.fields['destination_currency'].widget.attrs.update({'onchange': 'setamount()'})
    ######################## ProfileUpdate ##########################
    profile_form = ProfileForm()
    profile_form.fields['first_name'].widget.attrs.update({"value": request.user.first_name})
    profile_form.fields['last_name'].widget.attrs.update({"value": request.user.last_name})
    phone_number = UserProfile.objects.filter(user=request.user).first().phone_number
    profile_form.fields['phone_number'].widget.attrs.update({"value": phone_number})
    ######################## End ################
    orders = Order.objects.filter(user=request.user)
    response = {"title": "Dashboard", "coins": cached(getcoins)(), "dollar": cached(getdollar)(),
                "card_form": card_form,
                "Verification_Form": verification_form, "orders": orders, "Order_Form": order_form,
                "ProfileForm": profile_form, "is_verified": verified}
    print(response)
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
        return render(request, 'login.html', context={})


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
            return redirect('/accounts/dashboard/')
        else:
            messages.add_message(request, messages.ERROR, user_form.errors)
            redirect('/home/')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        user_form.fields['first_name'].widget.attrs.update({'placeholder': 'FirstName'})
        user_form.fields['first_name'].widget.attrs.update({'tabindex': 0})
        user_form.fields['last_name'].widget.attrs.update({'placeholder': 'LastName'})
        user_form.fields['username'].widget.attrs.update({'placeholder': 'UserName'})
        profile_form.fields['phone_number'].widget.attrs.update({'placeholder': 'PhoneNumber Ex: +98xxxxxxx'})
        user_form.fields['email'].widget.attrs.update({'placeholder': 'Email Ex: example@gmail.com'})
        user_form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        return render(request, 'signup.html',
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
            # except IntegrityError as error:
            #     messages.add_message(request, messages.ERROR, error)
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
            return redirect("/accounts/dashboard/")
        else:
            messages.add_message(request, messages.ERROR, verification_form.errors)
            return redirect("/accounts/dashboard/")
    else:
        messages.add_message(request, messages.ERROR, 'You Should USE POST METHOD IN REQUEST')
        return redirect("/accounts/dashboard/")


@login_required
@csrf_exempt
def verifyorder_page(request):
    if request.method == 'POST':
        order_Form = OrderForm(request.POST, cards=request.user, coins=coinsselector())
        if order_Form.is_valid():
            try:
                instance = order_Form.save()
                instance.user = request.user
                instance.status = "Pending"
                instance.save()
                messages.add_message(request, messages.SUCCESS,
                                     "Your Order Added Successfully")  # except IntegrityError as error:  # messages.add_message(request, messages.ERROR, error)
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
            return redirect("/accounts/dashboard/")
        else:
            messages.add_message(request, messages.ERROR, order_Form.errors)
        return redirect("/accounts/dashboard/")
    else:
        messages.add_message(request, messages.ERROR, 'You Should USE POST METHOD IN REQUEST')
        return redirect("/accounts/dashboard/")


def coinswithamount(request, coin):
    coins = cached(getcoins)()
    for k in coins["data"]:
        if int(k["rank"]) <= 20:
            if k["symbol"] == coin:
                return JsonResponse({'coin': coin, 'USD': k["priceUsd"], 'IRR': cached(getdollar)()})
    return HttpResponse("I Cant Found Your Coin")


@csrf_exempt
@login_required
def updateprofile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            try:
                userprofile_object = UserProfile.objects.get(user=request.user)
                userprofile_object.phone_number = profile_form.cleaned_data['phone_number']
                userprofile_object.save()
                user_object = User.objects.get(pk=request.user.id)
                user_object.first_name = profile_form.cleaned_data['first_name']
                user_object.last_name = profile_form.cleaned_data['last_name']
                user_object.save()
                messages.add_message(request, messages.SUCCESS,
                                     "Your Profile Updated Successfully")  # except IntegrityError as error:  # messages.add_message(request, messages.ERROR, error)
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
            return redirect("/accounts/dashboard/")
        else:
            messages.add_message(request, messages.ERROR, profile_form.errors)
        return redirect("/accounts/dashboard/")
    else:
        messages.add_message(request, messages.ERROR, 'You Should USE POST METHOD IN REQUEST')
        return redirect("/accounts/dashboard/")


@csrf_exempt
def sendmessage(request):
    if request.method == 'POST':
        messageform = MsgBoxForm(request.POST)
        if messageform.is_valid():
            try:
                messageform.save()
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
            return redirect("/home/")
        else:
            messages.add_message(request, messages.ERROR, messageform.errors)
        return redirect("/home/")
    else:
        messages.add_message(request, messages.ERROR, 'You Should USE POST METHOD IN REQUEST')
        return redirect("/home/")
