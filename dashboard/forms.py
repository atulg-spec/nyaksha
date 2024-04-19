from django import forms
from django.contrib.auth import get_user_model
from .models import *
User = get_user_model()

class LoginForm(forms.Form):
    email = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'border border-gray-300 text-gray-900 rounded focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2 px-3 disabled:opacity-50 disabled:pointer-events-none', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border border-gray-300 text-gray-900 rounded focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2 px-3 disabled:opacity-50 disabled:pointer-events-none', 'placeholder': '**********'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''  # Remove default colon after label
            field.widget.attrs.update({'class': 'inline-block mb-2'})  # Add class to label


class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'mb-2 border border-gray-300 text-gray-900 rounded focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2 px-3 disabled:opacity-50 disabled:pointer-events-none'})
            field.widget.label_attrs={'class': 'mb-2 block text-gray-800'}

    class Meta:
        model = contact_us
        fields = ['phone_number_or_email','subject','description']


class CustomUserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'mb-2 border border-gray-300 text-gray-900 rounded focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2 px-3 disabled:opacity-50 disabled:pointer-events-none'})
            field.widget.label_attrs={'class': 'mb-2 block text-gray-800'}
    class Meta:
        model = CustomUser
        fields = [
            'default_quantity',
            'crudeoil_quantity',
            'nifty_quantity',
            'bank_nifty_quantity',
            'fin_nifty_quantity',
            'bankex_quantity',
            'sensex_quantity',
        ]
