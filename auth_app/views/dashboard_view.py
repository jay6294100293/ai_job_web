from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Render the user dashboard with total cost and API preferences."""
    user = request.user
    return render(request, 'auth_app/dashboard.html', {
        'total_cost': user.total_cost,
        'preferred_api': user.preferred_api,
        'chatgpt_api_key': user.chatgpt_api_key,
        'gemini_api_key': user.gemini_api_key,
    })
