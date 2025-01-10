# models.py
from django.db import models
from django.utils import timezone
from auth_app.models import CustomUser


class JobInput(models.Model):
    """Model for storing job inputs and their associated data."""
    company_name = models.CharField(max_length=100)
    job_description = models.TextField()
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.user.email}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Input'
        verbose_name_plural = 'Job Inputs'


class KeywordExtraction(models.Model):
    """Model for storing keyword extraction results."""
    PROVIDER_CHOICES = [
        ('openai', 'OpenAI'),
        ('gemini', 'Gemini'),
    ]

    job_input = models.ForeignKey(JobInput, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    keywords = models.JSONField()
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        default=0
    )
    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        default='openai'
    )
    created_at = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_input.company_name} - {self.provider} Keywords"

    class Meta:
        ordering = ['-created_at']


class UserAPIUsage(models.Model):
    """Model for tracking API usage and costs."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    total_openai_cost = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        default=0
    )
    total_gemini_cost = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        default=0
    )
    total_extractions = models.PositiveIntegerField(default=0)
    last_extraction_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"API Usage - {self.user.email}"

    def update_usage(self, cost, provider):
        """Update usage statistics."""
        if provider == 'openai':
            self.total_openai_cost += cost
        else:
            self.total_gemini_cost += cost

        self.total_extractions += 1
        self.last_extraction_date = timezone.now()
        self.save()