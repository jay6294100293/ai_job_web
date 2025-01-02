from django import forms

from core.models import JobInput


class JobInputForm(forms.ModelForm):
    class Meta:
        model = JobInput
        fields = ['company_name', 'job_description', 'resume_file', 'resume_text']
