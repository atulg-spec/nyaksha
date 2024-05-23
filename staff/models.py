from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS = [
        ('initiated', 'initiated'),
        ('pending', 'pending'),
        ('completed', 'completed'),
    ]

class Sales(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    customer_name=models.CharField(max_length=100,default="")
    description=models.TextField(max_length=5000,default="")
    phone_number=models.CharField(max_length=100,default="")
    datetime = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        verbose_name = "Sales Data"
        verbose_name_plural = "Sales Data"
    def __str__(self):
        return self.phone_number

