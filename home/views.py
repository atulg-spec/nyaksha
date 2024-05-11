from django.shortcuts import render
from dashboard.forms import ContactUsForm
from django.contrib import messages

# Create your views here.
def contact(request):
    if request.method == 'POST':
        print('1')
        form = ContactUsForm(request.POST)
        if form.is_valid():
            print('2')
            ob = form.save(commit=False)
            if request.user.is_authenticated:
                ob.user = request.user
            ob.save()
            print('4')
            messages.success(request,'We have saved your request. Will try to contact to you as soon as possible.')
        else:
            print(form.errors)
    context = {
        'form':ContactUsForm()
    }
    return render(request,'home/contact.html',context)


def index(request):
    return render(request,'home/index.html')

def privacypolicy(request):
    return render(request,'home/privacypolicy.html')

def refundpolicy(request):
    return render(request,'home/refundpolicy.html')

def about(request):
    return render(request,'home/about.html')

def disclaimer(request):
    return render(request,'home/disclaimer.html')

def termsofuse(request):
    return render(request,'home/termsofuse.html')
