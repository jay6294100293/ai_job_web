from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from auth_app.forms.api_key_form import APIKeyForm


@login_required
def update_api_keys(request):
    if request.method == 'POST':
        form = APIKeyForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('job_input')
    else:
        form = APIKeyForm(instance=request.user)
    return render(request, 'auth_app/update_api_keys.html', {'form': form})