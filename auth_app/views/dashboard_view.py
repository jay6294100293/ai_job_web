# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
#
# @login_required
# def dashboard(request):
#     """Render the user dashboard with total cost and API preferences."""
#     user = request.user
#     return render(request, 'auth_app/dashboard.html', {
#         'total_cost': user.total_cost,
#         'preferred_api': user.preferred_api,
#         'chatgpt_api_key': user.chatgpt_api_key,
#         'gemini_api_key': user.gemini_api_key,
#     })

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import UserAPIUsage


@login_required
def dashboard(request):
    """Render the user dashboard with API usage costs and preferences."""
    user = request.user

    # Get or create UserAPIUsage for the user
    api_usage, created = UserAPIUsage.objects.get_or_create(user=user)

    # Calculate total cost across both providers
    total_cost = api_usage.total_openai_cost + api_usage.total_gemini_cost

    return render(request, 'auth_app/dashboard.html', {
        'total_cost': total_cost,
        'openai_cost': api_usage.total_openai_cost,
        'gemini_cost': api_usage.total_gemini_cost,
        'total_extractions': api_usage.total_extractions,
        'last_extraction_date': api_usage.last_extraction_date,
        'preferred_api': user.preferred_api,
        'chatgpt_api_key': user.chatgpt_api_key,
        'gemini_api_key': user.gemini_api_key,
    })