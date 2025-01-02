import openai
import requests

OPENAI_COST_PER_1K_TOKENS = 0.002  # Cost for gpt-3.5-turbo per 1,000 tokens
GEMINI_COST_PER_REQUEST = 0.001   # Placeholder cost for Gemini per request

def extract_keywords_with_openai(job_description, api_key, user):
    """Use OpenAI to extract keywords and calculate cost."""
    prompt = (
        "Extract the 10 most important keywords from the following job description:\n\n"
        f"{job_description}\n\n"
        "Provide the keywords as a comma-separated list."
    )
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    tokens_used = response['usage']['total_tokens']
    cost = (tokens_used / 1000) * OPENAI_COST_PER_1K_TOKENS

    # Update user's total cost
    user.total_cost += cost
    user.save()

    keywords = response['choices'][0]['text'].strip()
    return [keyword.strip() for keyword in keywords.split(',')], cost

def extract_keywords_with_gemini(job_description, api_key, user):
    """Use Gemini to extract keywords and calculate cost."""
    response = requests.post(
        "https://gemini.example.com/api/keywords",  # Replace with actual Gemini API URL
        json={"text": job_description},
        headers={"Authorization": f"Bearer {api_key}"}
    )
    if response.status_code == 200:
        cost = GEMINI_COST_PER_REQUEST
        # Update user's total cost
        user.total_cost += cost
        user.save()
        return response.json().get("keywords", []), cost
    else:
        raise Exception("Gemini API Error: " + response.text)
