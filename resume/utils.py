import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_ats_resume(data):
    prompt = f"""
You are a professional resume writer and ATS optimization expert.

Convert the following user data into an ATS-friendly professional resume.

Rules:
- Use simple headings
- No tables
- Bullet points only
- Strong action verbs
- Optimized for ATS
- Clean professional tone

User Data:
Name: {data['full_name']}
Email: {data['email']}
Phone: {data['phone']}
LinkedIn: {data['linkedin']}

Target Role: {data['target_role']}
Industry: {data['industry']}

Skills:
{data['skills']}

Experience:
{data['experience']}

Education:
{data['education']}
"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text