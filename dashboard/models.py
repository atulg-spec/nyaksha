from django.db import models
from django.contrib.auth.models import AbstractUser
from dashboard.manager import *
from django.utils import timezone
import json
from threading import Thread
import requests
from nyaksha.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import render_to_string


PLAN_CHOICES = [
        ('Free', 'Free'),
        ('Basic', 'Basic -> 10000'),
        ('Pro', 'Pro -> 15000'),
        ('VIP', 'VIP -> 20000'),
        ('Premium', 'Premium -> 30000'),
    ]


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    is_suscribed = models.BooleanField(default=False)
    plan_type = models.CharField(max_length=100,choices=PLAN_CHOICES,default="Free")
    suscribed_date = models.DateTimeField(auto_now_add=True,null=True)
    expiry_date = models.DateTimeField(default=timezone.now)
    default_quantity = models.PositiveIntegerField(blank=True, null=True,default=10)
    crudeoil_quantity = models.PositiveIntegerField(blank=True, null=True,default=100)
    nifty_quantity = models.PositiveIntegerField(blank=True, null=True,default=50)
    bank_nifty_quantity = models.PositiveIntegerField(blank=True, null=True,default=15)
    fin_nifty_quantity = models.PositiveIntegerField(blank=True, null=True,default=40)
    bankex_quantity = models.PositiveIntegerField(blank=True, null=True,default=40)
    sensex_quantity = models.PositiveIntegerField(blank=True, null=True,default=10)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 


class Webhook(models.Model):
    id=models.AutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True,null=True)
    url = models.CharField(max_length=100,default="")
    address = models.CharField(max_length=100,default="")
    class Meta:
        verbose_name = "Webhook Address"
        verbose_name_plural = "Webhook Address"
    def __str__(self):
       return self.address
    

from django.contrib.auth import get_user_model

User = get_user_model()

class Response(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    broker = models.CharField(max_length=50,default="")
    api_name = models.CharField(max_length=50,default="")
    response = models.CharField(max_length=1000,default="")
    response_2 = models.CharField(max_length=1000,default="")
    syntax_used = models.CharField(max_length=1000,default="")
    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"
    def __str__(self):
       return self.response


# CONTACT US
class contact_us(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    phone_number_or_email=models.CharField(max_length=100,default="")
    subject=models.CharField(max_length=100,default="")
    description=models.TextField(max_length=5000,default="")
    datetime = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
    def __str__(self):
        return self.phone_number_or_email


class brokers(models.Model):
    broker=models.CharField(max_length=100,default="")
    class Meta:
        verbose_name = "Broker"
        verbose_name_plural = "Brokers"
    def __str__(self):
        return self.broker
    
class users(models.Model):
    user=models.CharField(max_length=100,default="")
    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscription Types"
    def __str__(self):
        return self.user

SEGMENT_CHOICES = [
    ('NSE', 'NSE'),
    ('BSE', 'BSE'),
    ('NFO', 'NFO'),
    ('BFO', 'BFO'),
    ('MCX', 'MCX'),
]

OTYPE_CHOICES = [
    ('MARKET', 'MARKET'),
    ('LIMIT', 'LIMIT'),
]

PTYPE_CHOICES = [
    ('INTRADAY', 'INTRADAY'),
    ('NRML', 'NRML'),
    ('CNC', 'CNC'),
]

TTYPE_CHOICES = [
    ('BUY', 'BUY'),
    ('SELL', 'SELL'),
]

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    url = models.ForeignKey(Webhook, on_delete=models.CASCADE, null=True, blank=True)
    brokers = models.ManyToManyField(brokers, blank=True)
    segment = models.CharField(max_length=100, choices=SEGMENT_CHOICES, default="NSE")
    symbol = models.CharField(max_length=100, default="")
    token = models.CharField(max_length=100, default="")
    price = models.CharField(max_length=100, default="0")
    order_type = models.CharField(max_length=100, choices=OTYPE_CHOICES, default="MARKET")
    product_type = models.CharField(max_length=100, choices=PTYPE_CHOICES, default="NRML")
    transaction_type = models.CharField(max_length=100, choices=TTYPE_CHOICES, default="BUY")
    stoploss = models.CharField(max_length=100, default="0")
    target = models.CharField(max_length=100, default="0")
    users = models.ManyToManyField(users, blank=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being saved for the first time
            # Save the instance to generate an ID before accessing many-to-many relationships
            super().save(*args, **kwargs)

        broker_names = ', '.join(str(broker) for broker in self.brokers.all())
        user_names = ', '.join(str(user) for user in self.users.all())

        syntax = {
            "syntaxcount": 1,
            "syntax1": {
                "broker": broker_names,
                "variety": "NORMAL",
                "segment": self.segment,
                "symbol": self.symbol,
                "token": self.token,
                "price": self.price,
                "otype": self.order_type,
                "ptype": self.product_type,
                "ttype": self.transaction_type,
                "position": "OPEN",
                "stoploss": self.stoploss,
                "target": self.target,
                "trailing_sl": "",
                "extype": "C",
                "option": "False",
                "callput": "",
                "gap": "+200",
                "rate": "100",
                "users": user_names
            }
        }
        thread = Thread(target=place_order,args=(syntax,self.url.address))
        thread.start()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.symbol


def place_order(syntax,url):
    data = json.dumps(syntax)
    print(data)
    response = requests.post(url, data)




# SIGNALS 
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if True:
        print('created')
        subject = "Welcome to Nyaksha - Complete Your Profile Setup!"
        print(instance.first_name)
        context = {
            'user':instance.first_name,
        }
        html_content = render_to_string('welcome-email.html', context)
        content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject,
            content ,
            EMAIL_HOST_USER ,
            [instance.email]
        )
        email.attach_alternative(html_content,'text/html')
        email.send()