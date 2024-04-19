from django import forms
from .models import *

class AngelOneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'mb-2 border border-gray-300 text-gray-900 rounded focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2 px-3 disabled:opacity-50 disabled:pointer-events-none'})
            # Add class to labels
            field.widget.label_attrs={'class': 'mb-2 block text-gray-800'}

    class Meta:
        model = angel_api
        fields = ['api_name','api_key','client_id','m_pin','t_otp_token']



class DhanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'mb-2 border border-gray-300 text-gray-900 rounded focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2 px-3 disabled:opacity-50 disabled:pointer-events-none'})
            # Add class to labels
            field.widget.label_attrs={'class': 'mb-2 block text-gray-800'}

    class Meta:
        model = dhan_api
        fields = ['api_name','client_id','access_token']