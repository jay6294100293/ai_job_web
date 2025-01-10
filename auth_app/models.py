from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    chatgpt_api_key = models.CharField(max_length=255, blank=True, null=True)
    gemini_api_key = models.CharField(max_length=255, blank=True, null=True)
    preferred_api = models.CharField(
        max_length=10,
        choices=[('openai', 'OpenAI'), ('gemini', 'Gemini')],
        default='openai'
    )
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Custom related name to avoid clashes
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Custom related name to avoid clashes
        blank=True,
    )

