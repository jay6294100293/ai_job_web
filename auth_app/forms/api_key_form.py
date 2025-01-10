from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from auth_app.models import CustomUser


class APIKeyForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['chatgpt_api_key', 'gemini_api_key','preferred_api']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user