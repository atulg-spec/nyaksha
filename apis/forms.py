from django import forms
from .models import *

class AngelOneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = angel_api
        fields = ['api_name','api_key','client_id','m_pin','t_otp_token']
