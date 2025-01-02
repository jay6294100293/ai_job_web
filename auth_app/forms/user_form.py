from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from auth_app.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="First Name")
    last_name = forms.CharField(max_length=150, required=True, label="Last Name")
    class Meta:
        model = CustomUser
        fields = ["first_name","last_name",'username', 'email', 'password1', 'password2']
