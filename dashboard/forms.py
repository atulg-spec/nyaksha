from django import forms
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '**********'}))


class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = contact_us
        fields = ['phone_number_or_email','subject','description']