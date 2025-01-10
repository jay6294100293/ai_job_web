from django import forms

from core.models import JobInput


class JobInputForm(forms.ModelForm):
    resume_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Paste your resume here',
            'class': 'mt-2 block w-full h-32 p-3 border rounded-lg focus:ring-blue-500 focus:border-blue-500',
        })
    )

    class Meta:
        model = JobInput
        fields = ['company_name', 'job_description', 'resume_file', 'resume_text']

    def clean(self):
        cleaned_data = super().clean()
        resume_file = cleaned_data.get('resume_file')
        resume_text = cleaned_data.get('resume_text')

        if not resume_file and not resume_text:
            raise forms.ValidationError("You must either upload a resume file or paste your resume text.")

        return cleaned_data
