from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from auth_app.models import CustomUser


class APIKeyForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['chatgpt_api_key', 'gemini_api_key']