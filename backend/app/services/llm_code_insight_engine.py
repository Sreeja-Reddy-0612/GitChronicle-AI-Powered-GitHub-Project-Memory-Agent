import os
from google import genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMCodeInsightEngine:

    def __init__(self):
        # We initialize APIs. It automatically picks up API keys from environment.
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        self.openai_client = None
        if self.openai_api_key:
            self.openai_client = OpenAI()

        self.gemini_client = None
        if self.gemini_api_key:
            self.gemini_client = genai.Client(api_key=self.gemini_api_key)

    def generate_summary(self, files):
        summaries = []

        for f in files:
            name = f.get("filename", "")

            if name.endswith(".py"):
                summaries.append(f"{name} contains backend logic or API handling.")
            elif name.endswith(".jsx") or name.endswith(".tsx"):
                summaries.append(f"{name} is a frontend UI component.")
            elif name.endswith(".md"):
                summaries.append(f"{name} updates documentation.")
            else:
                summaries.append(f"{name} was modified.")

        return summaries

    def process_commits(self, commits):
        for commit in commits:
            files = commit.get("files", [])
            commit["code_insights"] = self.generate_summary(files)
        return commits

    def analyze_commit(self, owner, repo, sha, message, patch):
        if not self.openai_client and not self.gemini_client:
            return "LLM disabled: Neither OPENAI_API_KEY nor GEMINI_API_KEY is set in the environment."

        if not patch:
            return "No file changes found in this commit to analyze."

        from app.utils.vector_store import JSONVectorStore
        
        # Retrieve broader repository context using the commit SHA and initial patch lines
        query_text = f"Context for commit {sha[:7]}: {message}"
        try:
            vector_store = JSONVectorStore()
            # Fetch chunks specifically tagged with this SHA
            context_chunks = vector_store.search(owner, repo, query_text, sha=sha, top_k=8)
            context_text = "\n\n---\n\n".join(context_chunks)
        except Exception as e:
            context_text = f"Context retrieval failed: {e}"

        import json
        import re

        def clean_text(text):
            # Remove markdown headers like ## or ###
            text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
            # Remove bullet points like * or - at the start of lines
            text = re.sub(r'^\s*[\*\-]\s*', '', text, flags=re.MULTILINE)
            # Bold headings (words ending with colon or similar) -> actually the user said "give heading in bold"
            # If the LLM provides headers, we can try to bold them if they aren't already.
            # But the user specifically said "for heading i am getting ##'s before them... remove those, give heading in bold"
            # So I will look for lines that look like headings and wrap them in ** ** if they are not already.
            # A simple heuristic: a line that doesn't end with a period and is short, or starts with a capitalized word and ends with a colon.
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if line.strip().endswith(':') and not line.strip().startswith('**'):
                    lines[i] = f"**{line.strip()}**"
            return '\n'.join(lines).strip()

        prompt = f"""
You are an expert Senior Software Engineer explaining a commit.
I will provide you with a commit message, the git patch containing the code changes, and additional retrieved code context (chunks).

Your task is to explain this code by returning a JSON object with the following structure:
{{
  "overall_summary": "A concise developer-level summary of the entire commit.",
  "file_insights": {{
    "path/to/file1.py": "Specific explanation for this file, its role, and logic changes.",
    "path/to/file2.js": "Specific explanation for this file..."
  }}
}}

STRICT RULES:
1. Return ONLY the JSON object. No other text.
2. The "file_insights" keys must match the filenames provided in the patch exactly.
3. Do not use markdown headers (##) or bullet points (*) in your explanations. 
4. If a file is a new component, explain its purpose. If it's a modification, explain the change.

Context:
{context_text}

Commit Message:
{message}

Patch Data:
{patch}
"""

        try:
            raw_response = ""
            if self.gemini_client:
                models_to_try = ['gemini-2.5-flash', 'gemini-2.5-pro']
                for model_name in models_to_try:
                    try:
                        response = self.gemini_client.models.generate_content(
                            model=model_name,
                            contents=prompt
                        )
                        raw_response = response.text
                        break
                    except Exception as e:
                        if model_name == models_to_try[-1]:
                            raise e
                        continue
            else:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a senior developer. Respond ONLY with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1
                )
                raw_response = response.choices[0].message.content

            # Parse JSON
            # Sometimes LLMs wrap JSON in code blocks
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
            else:
                data = json.loads(raw_response)

            # Sanitize and Clean
            data["overall_summary"] = clean_text(data.get("overall_summary", ""))
            insights = data.get("file_insights", {})
            for filename in insights:
                insights[filename] = clean_text(insights[filename])
            
            return data

        except Exception as e:
            return {
                "overall_summary": f"Analysis failed: {str(e)}",
                "file_insights": {}
            }
        except Exception as e:
            return f"LLM Analysis failed due to an error: {str(e)}"