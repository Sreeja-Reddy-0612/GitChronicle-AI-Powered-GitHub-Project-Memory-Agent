import requests
import os
from dotenv import load_dotenv

load_dotenv()


class GitHubClient:

    def __init__(self):
        self.base_url = "https://api.github.com"

        token = os.getenv("GITHUB_TOKEN")

        self.headers = {
            "Authorization": f"token {token}" if token else ""
        }

    # ✅ EXISTING FUNCTION
    def get_commits(self, owner, repo):

        url = f"{self.base_url}/repos/{owner}/{repo}/commits"

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()

    # 🔥🔥 ADD THIS (CRITICAL FIX)
    def get_commit_details(self, owner, repo, sha):

        url = f"{self.base_url}/repos/{owner}/{repo}/commits/{sha}"

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(response.text)

        data = response.json()

        commit_data = data.get("commit", {})
        author_data = commit_data.get("author", {})

        files = []
        for f in data.get("files", []):
            files.append({
                "filename": f.get("filename"),
                "patch": f.get("patch", ""),
                "changes": f.get("changes", 0)
            })

        return {
            "sha": data.get("sha"),
            "message": commit_data.get("message"),
            "author": author_data.get("name"),
            "date": author_data.get("date"),
            "url": data.get("html_url"),
            "files": files
        }

    def get_file_content(self, owner, repo, path, ref="main"):
        # Fetches the raw content of a file at a specific branch/commit
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}?ref={ref}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            return "" # Or handle error
            
        import base64
        data = response.json()
        if isinstance(data, dict) and "content" in data:
            try:
                return base64.b64decode(data["content"]).decode('utf-8')
            except Exception:
                return "[Binary File: Content cannot be displayed]"
        return ""