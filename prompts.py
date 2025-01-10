# prompts.py
ATS_KEYWORD_PROMPT = """Analyze this job description as an ATS expert to extract most important keywords.

Focus on extracting:
1. Technical skills and programming languages
2. Required certifications and qualifications
3. Industry-standard tools and technologies
4. Years of experience if specified
5. Key technical responsibilities

Rules:
- Extract terms EXACTLY as they appear in the job description
- Include both full terms and abbreviations (e.g., 'Python Django Framework (Django)')
- Maintain exact capitalization for technical terms (e.g., SQL, AWS, React.js)
- Prioritize technical skills over soft skills

Job Description:
{job_description}

Return ONLY a comma-separated list of exactly 10 keywords, no additional text."""