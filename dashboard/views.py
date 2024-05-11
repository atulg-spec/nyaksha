from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import *
from django.conf import settings
import json
from .forms import *
from dashboard.alerts.angel import angel_order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from apis.models import angel_api
from django.utils import timezone
from datetime import datetime,timedelta
import pyotp
try:
    from SmartApi import SmartConnect 
except:
    from smartapi import SmartConnect 

User = get_user_model()

# Create your views here.
def handle_login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard')
            else:
                messages.error(request, 'Invalid login credentials.')
                messages.info(request, 'Try Continuing with Google.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    angelone = angel_api.objects.filter(user=request.user)
    context = {
        'angelone':angelone,
    }
    return render(request,'dashboard.html',context)

@login_required
def plans(request):
    context = {
    }
    return render(request,'plans.html',context)

@login_required
def contactus(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            ob = form.save(commit=False)
            ob.user = request.user
            ob.save()
            messages.success(request,'We have saved your request. Will try to contact to you as soon as possible.')
    context = {
        'form':ContactUsForm()
    }
    return render(request,'contact.html',context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')  # Redirect to user's profile page after successful update
    else:
        form = CustomUserUpdateForm(instance=request.user)
    context = {
        'form':form,
    }
    return render(request,'profile.html',context)


@login_required
def history(request):
    angelone = angel_api.objects.filter(user=request.user)
    holdings = []
    total_pnl = 0
    for x in angelone:
        try:
            smartApi = SmartConnect(x.api_key)
            try:
                token = x.t_otp_token
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                pass
            data = smartApi.generateSession(x.client_id, x.m_pin, totp)
            hold = smartApi.position()
            if hold['data'] is None:
                continue
            holdings.append(hold)
            for i in hold['data']:
                total_pnl = total_pnl + i['reliased']
        except Exception as e:
            print(e)
            messages.error(request,f'Your Angel ONE api {x.api_name} credentials are Invalid. Please delete it to avoid any crashes.')
    context = {
        'holdings':holdings,
        'total_pnl':round(total_pnl,2),
    }
    return render(request,'history.html',context)



@login_required
def portfolio(request):
    angelone = angel_api.objects.filter(user=request.user)
    holdings = []
    total_pnl = 0
    total_pnl_per = 0
    for x in angelone:
        try:
            smartApi = SmartConnect(x.api_key)
            try:
                token = x.t_otp_token
                totp = pyotp.TOTP(token).now()
            except Exception as e:
                pass
            data = smartApi.generateSession(x.client_id, x.m_pin, totp)
            hold = smartApi.holding()
            if hold['data'] is None:
                continue
            holdings.append(hold)
            for i in hold['data']:
                total_pnl = total_pnl + i['profitandloss']
                total_pnl_per = total_pnl_per + i['pnlpercentage']
        except:
            messages.error(request,f'Your Angel ONE api {x.api_name} credentials are Invalid. Please delete it to avoid any crashes.')
    context = {
        'holdings':holdings,
        'total_pnl':round(total_pnl,2),
        'total_pnl_per':round(total_pnl_per,2),
    }
    return render(request,'portfolio.html',context)


@login_required
def performance(request):
    return render(request,'soon.html')


@login_required
def indicator(request):
    return render(request,'indicator.html')

# WEBHOOK ALERT
@csrf_exempt
def webhook(request,url):
    if request.method == 'POST':
        ob = Webhook.objects.filter(url = url)
        if ob.__len__() == 0:
            return redirect("/")
        status= ""
        json_data = json.loads(request.body)
        syntaxcount = json_data["syntaxcount"]
        count = 1
        err = ""
        while(count <= syntaxcount):
            syntax = "syntax"+str(count)
            broker = json_data[syntax]["broker"]
            if "Angel" in broker:
                angel_order(syntax,json_data)
            count = count+1
        return HttpResponse(status)
    else:
        return redirect('/')
# ---------END WEBHOOK-------------


# PAGES 
def handlelogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('/')

def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)
