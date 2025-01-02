from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.forms.job_input_form import JobInputForm


@login_required
def job_input(request):
    if request.method == 'POST':
        form = JobInputForm(request.POST, request.FILES)
        if form.is_valid():
            job_input = form.save(commit=False)
            job_input.user = request.user
            job_input.save()
            return redirect('extract_keywords', job_input_id=job_input.id)
    else:
        form = JobInputForm()
    return render(request, 'core/job_input.html', {'form': form})