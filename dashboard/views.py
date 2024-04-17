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
        request.user.default_quantity = request.POST.get('default_quantity')
        request.user.crudeoil_quantity = request.POST.get('crudeoil_quantity')
        request.user.nifty_quantity = request.POST.get('nifty_quantity')
        request.user.bank_nifty_quantity = request.POST.get('bank_nifty_quantity')
        request.user.fin_nifty_quantity = request.POST.get('fin_nifty_quantity')
        request.user.bankex_quantity = request.POST.get('bankex_quantity')
        request.user.sensex_quantity = request.POST.get('sensex_quantity')
        request.user.save()
    return render(request,'profile.html')


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
def privacypolicy(request):
    return render(request,'privacypolicy.html')

def refundpolicy(request):
    return render(request,'refundpolicy.html')

def about(request):
    return render(request,'about.html')

def disclaimer(request):
    return render(request,'disclaimer.html')

def termsofuse(request):
    return render(request,'termsofuse.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('/login')