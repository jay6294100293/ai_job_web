from django.db import models

# Create your models here.
from django.db import models
from auth_app.models import CustomUser  # Import from auth_app

class JobInput(models.Model):
    company_name = models.CharField(max_length=100)
    job_description = models.TextField()
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name
