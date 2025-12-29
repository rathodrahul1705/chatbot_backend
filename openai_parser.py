import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load environment variables FIRST
load_dotenv()

# ✅ Read API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY not found. Please set it in your .env file."
    )

# ✅ Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def parse_resume(text: str):
    prompt = f"""
You are a resume parser.

Return ONLY valid JSON.
DO NOT add explanations.
DO NOT use markdown.
DO NOT wrap in ```json.

Required JSON structure:
{{
  "Name": "",
  "Email": "",
  "Phone Number": "",
  "Skills": [],
  "Years of Experience": "",
  "Education": "",
  "Current/Last Job": "",
  "Companies Worked At": [],
  "LinkedIn": "",
  "Certifications": [],
  "Location": ""
}}

Resume Text:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # 🔥 Safety: remove markdown/code blocks if any
    content = re.sub(r"```json|```", "", content).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse resume",
            "raw_response": content
        }
