import requests
import os
from dotenv import load_dotenv

load_dotenv()


class GitHubClient:

    def __init__(self):
        self.base_url = "https://api.github.com"

        token = os.getenv("GITHUB_TOKEN")

        print("TOKEN:", token)  # 🔥 DEBUG

        self.headers = {
            "Authorization": f"token {token}" if token else ""
        }

    def get_commits(self, owner, repo):

        url = f"{self.base_url}/repos/{owner}/{repo}/commits"

        response = requests.get(url, headers=self.headers)

        print("STATUS:", response.status_code)
        print("RAW:", response.text[:300])

        if response.status_code != 200:
            raise Exception(response.text)

        commits = response.json()

        detailed_commits = []

        for commit in commits[:5]:

            sha = commit.get("sha")

            commit_data = commit.get("commit", {})
            author_data = commit_data.get("author", {})

            message = commit_data.get("message")
            author = author_data.get("name")
            date = author_data.get("date")
            html_url = commit.get("html_url")

            # 🔥 FETCH FILE PATCHES
            detail_url = f"{self.base_url}/repos/{owner}/{repo}/commits/{sha}"
            detail_res = requests.get(detail_url, headers=self.headers)

            files = []

            if detail_res.status_code == 200:
                detail_data = detail_res.json()

                for f in detail_data.get("files", []):
                    files.append({
                        "filename": f.get("filename"),
                        "patch": f.get("patch", ""),
                        "changes": f.get("changes", 0)
                    })

            detailed_commits.append({
                "sha": sha,
                "message": message,
                "author": author,
                "date": date,
                "url": html_url,
                "files": files
            })

        return detailed_commits