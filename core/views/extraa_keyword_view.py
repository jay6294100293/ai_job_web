from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from utils import extract_keywords_with_openai, extract_keywords_with_gemini
from ..models import JobInput


@login_required
def extract_keywords_view(request, job_input_id):
    job_input = get_object_or_404(JobInput, id=job_input_id)
    user = request.user

    if user.preferred_api == 'openai':
        api_key = user.chatgpt_api_key
        keywords, cost = extract_keywords_with_openai(job_input.job_description, api_key, user)
    elif user.preferred_api == 'gemini':
        api_key = user.gemini_api_key
        keywords, cost = extract_keywords_with_gemini(job_input.job_description, api_key, user)
    else:
        keywords, cost = [], 0.0

    return render(request, 'core/keywords.html', {
        'keywords': keywords,
        'cost': cost,
        'total_cost': user.total_cost
    })
