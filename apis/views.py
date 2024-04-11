from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages


@login_required
def angelone(request):
    if request.method == 'POST':
        form = AngelOneForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request,'API logged in successfully')
            return redirect('/dashboard')
        else:
            errors = form.errors.items()
            for x in errors:
                messages.error(request,f'{x}')
    context = {
        'form':AngelOneForm()
    }
    return render(request,'api/angelone.html',context)


@login_required
def status(request,broker,id):
    if broker == 'angel':
        try:
            ob = angel_api.objects.get(user=request.user,id=id)
            if ob.is_trading:
                ob.is_trading = False
                ob.save()
            else:
                ob.is_trading = True
                ob.save()
            messages.success(request,'API updated Successfully')
        except:
            pass
    return redirect('/dashboard')


@login_required
def delete(request,broker,id):
    if broker == 'angel':
        try:
            ob = angel_api.objects.get(user=request.user,id=id)
            ob.delete()
            messages.success(request,'API deleted successfully')
        except:
            pass
    return redirect('/dashboard')