from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import pyotp
try:
    from SmartApi import SmartConnect 
except:
    from smartapi import SmartConnect 


User = get_user_model()

class angel_api(models.Model):
    id=models.AutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    api_name = models.CharField(max_length=100,default="")
    api_key = models.CharField(max_length=100,default="")
    client_id = models.CharField(max_length=100,default="")
    m_pin = models.CharField(max_length=100,default="")
    t_otp_token = models.CharField(max_length=100,default="")
    is_trading = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Angel ONE API"
        verbose_name_plural = "Angel ONE API"
        unique_together = [['api_name', 'api_key', 'client_id', 'm_pin', 't_otp_token'],['user', 'api_name'],['client_id', 'm_pin', 't_otp_token']]
    def __str__(self):
       return self.api_name
    
    def clean(self):
        smartApi = SmartConnect(self.api_key)
        try:
            token = self.t_otp_token
            totp = pyotp.TOTP(token).now()
        except Exception as e:
            raise ValidationError("Invalid TOTP token")
        data = smartApi.generateSession(self.client_id, self.m_pin, totp)
        if data['status'] == False:
            print(data)
            raise ValidationError("Invalid Login Credentials")
        else:
            print(data)

