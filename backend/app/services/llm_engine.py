import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMEngine:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def explain_commit(self, commit):

        files_text = ""

        for f in commit.get("files", [])[:5]:  # limit files
            files_text += f"""
File: {f.get("filename")}
Changes:
{f.get("patch", "")[:1000]}
-------------------
"""

        prompt = f"""
You are a senior software engineer.

Analyze this commit:

Message: {commit.get("message")}

Files:
{files_text}

Return JSON list:

[
  {{
    "file": "filename",
    "role": "...",
    "what_changed": "...",
    "why_changed": "...",
    "impact": "..."
  }}
]
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            return response.choices[0].message.content

        except Exception as e:
            print("LLM ERROR:", e)
            return "[]"