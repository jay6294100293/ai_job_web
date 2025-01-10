# from decimal import Decimal
#
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.core.exceptions import ValidationError
# from django.shortcuts import render, get_object_or_404
# from core.models import JobInput
# from utils import extract_keywords_with_openai, extract_keywords_with_gemini, logger
#
#
# @login_required
# def extract_keywords_view(request, job_input_id):
#     """
#     View to extract keywords from a job description using the selected API.
#     """
#     job_input = get_object_or_404(JobInput, id=job_input_id, user=request.user)
#     user = request.user
#
#     # Check preferred API and corresponding API key
#     api_key = (
#         user.chatgpt_api_key
#         if user.preferred_api == "openai"
#         else user.gemini_api_key
#     )
#
#     if not api_key:
#         messages.error(
#             request,
#             f"Please set your {user.preferred_api.upper()} API key in your account settings."
#         )
#         return render(request, 'core/keywords_error.html', {
#             'error_message': "API key is missing. Please update your API key and try again."
#         })
#
#     try:
#         # Extract keywords based on the preferred API
#         keywords, cost = [], Decimal('0.0')
#         if user.preferred_api == 'openai':
#             keywords, cost = extract_keywords_with_openai(
#                 job_input.job_description,
#                 api_key,
#                 user
#             )
#         else:
#             keywords, cost = extract_keywords_with_gemini(
#                 job_input.job_description,
#                 api_key,
#                 user
#             )
#
#         if not keywords:
#             messages.error(request, "Failed to extract keywords. Please try again.")
#             return render(request, 'core/keywords_error.html', {
#                 'error_message': "No keywords were extracted. Please check the API key and job description."
#             })
#
#         messages.success(request, f"Successfully extracted {len(keywords)} keywords!")
#
#         return render(request, 'core/keywords.html', {
#             'job_input': job_input,
#             'keywords': keywords,
#             'cost': cost,
#             'total_cost': user.total_cost,
#             'api_provider': user.preferred_api.upper()
#         })
#
#     except ValidationError as e:
#         messages.error(request, str(e))
#         return render(request, 'core/keywords_error.html', {
#             'error_message': str(e)
#         })
#     except Exception as e:
#         logger.error(f"Keyword extraction error: {str(e)}", exc_info=True)
#         messages.error(request, "An unexpected error occurred during keyword extraction.")
#         return render(request, 'core/keywords_error.html', {
#             'error_message': "Please try again later or contact support if the problem persists."
#         })
#

from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from core.models import JobInput, KeywordExtraction, UserAPIUsage
from utils import extract_keywords_with_openai, extract_keywords_with_gemini, logger


@login_required
def extract_keywords_view(request, job_input_id):
    """
    View to extract keywords from a job description using the selected API.
    """
    job_input = get_object_or_404(JobInput, id=job_input_id, user=request.user)
    user = request.user

    # Check preferred API and corresponding API key
    api_key = (
        user.chatgpt_api_key
        if user.preferred_api == "openai"
        else user.gemini_api_key
    )

    if not api_key:
        messages.error(
            request,
            f"Please set your {user.preferred_api.upper()} API key in your account settings."
        )
        return render(request, 'core/keywords_error.html', {
            'error_message': "API key is missing. Please update your API key and try again."
        })

    try:
        # Extract keywords based on the preferred API
        keywords, cost = [], Decimal('0.0')
        if user.preferred_api == 'openai':
            keywords, cost = extract_keywords_with_openai(
                job_input.job_description,
                api_key,
                user
            )
        else:
            keywords, cost = extract_keywords_with_gemini(
                job_input.job_description,
                api_key,
                user
            )

        if not keywords:
            messages.error(request, "Failed to extract keywords. Please try again.")
            return render(request, 'core/keywords_error.html', {
                'error_message': "No keywords were extracted. Please check the API key and job description."
            })

        # Save successful extraction
        keyword_extraction = KeywordExtraction.objects.create(
            job_input=job_input,
            user=user,
            keywords=keywords,
            cost=cost,
            provider=user.preferred_api,
            success=True
        )

        # Update user's API usage
        api_usage, _ = UserAPIUsage.objects.get_or_create(user=user)
        api_usage.update_usage(cost, user.preferred_api)

        messages.success(request, f"Successfully extracted {len(keywords)} keywords!")
        return render(request, 'core/keywords.html', {
            'job_input': job_input,
            'keywords': keywords,
            'cost': cost,
            'total_cost': user.total_cost,
            'api_provider': user.preferred_api.upper(),
            'extraction_id': keyword_extraction.id
        })

    except ValidationError as e:
        messages.error(request, str(e))
        return render(request, 'core/keywords_error.html', {
            'error_message': str(e)
        })

    except Exception as e:
        logger.error(f"Keyword extraction error: {str(e)}", exc_info=True)
        messages.error(request, "An unexpected error occurred during keyword extraction.")
        return render(request, 'core/keywords_error.html', {
            'error_message': "Please try again later or contact support if the problem persists."
        })