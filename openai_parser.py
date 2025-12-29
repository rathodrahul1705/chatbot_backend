from openai import OpenAI
import json
import os
import re

client = OpenAI(api_key="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")

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
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # 🔥 Remove markdown if model still adds it
    content = re.sub(r"```json|```", "", content).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse resume",
            "raw_response": content
        }
