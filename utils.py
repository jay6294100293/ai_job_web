# import requests
# # Define message tags for styling
#
#
# from django.contrib.messages import constants as messages
#
# OPENAI_COST_PER_1K_TOKENS = 0.002  # Cost for gpt-3.5-turbo per 1,000 tokens
# GEMINI_COST_PER_REQUEST = 0.001   # Placeholder cost for Gemini per request
#
# from openai import OpenAI  # New import syntax
#
#
# def extract_keywords_with_openai(job_description, api_key, user):
#     """
#     Use OpenAI ChatCompletion API to extract keywords and calculate the cost.
#     """
#     prompt = (
#         "Extract the 10 most important keywords from the following job description:\n\n"
#         f"{job_description}\n\n"
#         "Provide the keywords as a comma-separated list."
#     )
#
#     # Initialize the client
#     client = OpenAI(api_key=api_key)
#
#     try:
#         # Call the OpenAI ChatCompletion API with new syntax
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=500,
#         )
#
#         # Calculate cost based on token usage
#         tokens_used = response.usage.total_tokens
#         cost = (tokens_used / 1000) * OPENAI_COST_PER_1K_TOKENS
#
#         # Update the user's total cost
#         user.total_cost += cost
#         user.save()
#
#         # Extract keywords from the response
#         keywords = response.choices[0].message.content.strip()
#         return [keyword.strip() for keyword in keywords.split(',')], cost
#
#     except Exception as e:
#         # Log the error and return empty results
#         print(f"OpenAI API error: {e}")
#         return [], 0.0
#
# def extract_keywords_with_gemini(job_description, api_key, user):
#     """Use Gemini to extract keywords and calculate cost."""
#     response = requests.post(
#         "https://gemini.example.com/api/keywords",  # Replace with actual Gemini API URL
#         json={"text": job_description},
#         headers={"Authorization": f"Bearer {api_key}"}
#     )
#     if response.status_code == 200:
#         cost = GEMINI_COST_PER_REQUEST
#         # Update user's total cost
#         user.total_cost += cost
#         user.save()
#         return response.json().get("keywords", []), cost
#     else:
#         raise Exception("Gemini API Error: " + response.text)
import google.generativeai as genai
import logging
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from openai import OpenAI
from typing import Tuple, List
import requests
from django.contrib.messages import constants as messages

from prompts import ATS_KEYWORD_PROMPT

# Configure logging
logger = logging.getLogger(__name__)

# Constants should be in settings.py
OPENAI_COST_PER_1K_TOKENS = Decimal('0.002')  # Using Decimal for financial calculations
GEMINI_COST_PER_REQUEST = Decimal('0.001')

import logging
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from typing import Tuple, List
from openai import OpenAI
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Constants
OPENAI_COST_PER_1K_TOKENS = Decimal('0.002')
GEMINI_COST_PER_REQUEST = Decimal('0.001')


def extract_keywords_with_openai(
        job_description: str,
        api_key: str,
        user: 'User'
) -> Tuple[List[str], Decimal]:
    """
    Extract keywords from job description using OpenAI API.

    Args:
        job_description: The job description text
        api_key: OpenAI API key
        user: User model instance

    Returns:
        Tuple containing list of keywords and the cost

    Raises:
        ValidationError: If API call fails
    """
    if not job_description:
        raise ValidationError("Job description cannot be empty")

    prompt = ATS_KEYWORD_PROMPT.format(job_description=job_description)
    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an expert ATS system analyst specializing in technical job descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3,  # Lower temperature for more consistent results
        )

        # Calculate cost
        tokens_used = response.usage.total_tokens
        cost = Decimal(tokens_used) / 1000 * OPENAI_COST_PER_1K_TOKENS

        # Update user cost using atomic transaction
        with transaction.atomic():
            user.total_cost = user.total_cost + cost
            user.save()

        # Process keywords
        keywords = [
            keyword.strip()
            for keyword in response.choices[0].message.content.split(',')
            if keyword.strip()
        ]

        # Ensure exactly 10 keywords
        keywords = keywords[:10] if len(keywords) > 10 else keywords

        return keywords, cost

    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
        raise ValidationError(f"Failed to extract keywords: {str(e)}")


def extract_keywords_with_gemini(
        job_description: str,
        api_key: str,
        user: 'User'
) -> Tuple[List[str], Decimal]:
    """
    Extract keywords using Gemini API.

    Args:
        job_description: The job description text
        api_key: Gemini API key
        user: User model instance

    Returns:
        Tuple containing list of keywords and the cost

    Raises:
        ValidationError: If API call fails
    """
    if not job_description:
        raise ValidationError("Job description cannot be empty")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = ATS_KEYWORD_PROMPT.format(job_description=job_description)
        response = model.generate_content(prompt)

        if not response.text:
            raise ValidationError("Empty response from Gemini API")

        # Update user cost using atomic transaction
        with transaction.atomic():
            user.total_cost = user.total_cost + GEMINI_COST_PER_REQUEST
            user.save()

        # Process keywords
        keywords = [
            keyword.strip()
            for keyword in response.text.split(',')
            if keyword.strip()
        ]

        # Ensure exactly 10 keywords
        keywords = keywords[:10] if len(keywords) > 10 else keywords

        return keywords, GEMINI_COST_PER_REQUEST

    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}", exc_info=True)
        raise ValidationError(f"Failed to extract keywords: {str(e)}")


MESSAGE_TAGS = {
    messages.SUCCESS: 'bg-green-500 text-white p-3 rounded-lg',
    messages.ERROR: 'bg-red-500 text-white p-3 rounded-lg',
}