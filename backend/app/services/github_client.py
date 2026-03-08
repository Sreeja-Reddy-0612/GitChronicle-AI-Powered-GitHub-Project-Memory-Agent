import requests
from app.config import GITHUB_TOKEN, GITHUB_API_BASE


class GitHubClient:

    def __init__(self):
        self.base_url = GITHUB_API_BASE
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_commits(self, owner: str, repo: str, per_page: int = 30):
        """
        Fetch commit history from GitHub repository
        """

        url = f"{self.base_url}/repos/{owner}/{repo}/commits"

        params = {
            "per_page": per_page
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.text}")

        commits = response.json()

        processed_commits = []

        for commit in commits:

            processed_commits.append({
                "sha": commit["sha"],
                "message": commit["commit"]["message"],
                "author": commit["commit"]["author"]["name"],
                "date": commit["commit"]["author"]["date"],
                "url": commit["html_url"]
            })

        return processed_commits

    def get_commit_details(self, owner: str, repo: str, sha: str):
        """
        Fetch file-level changes for a specific commit
        """

        url = f"{self.base_url}/repos/{owner}/{repo}/commits/{sha}"

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            return []

        data = response.json()

        files = data.get("files", [])

        file_changes = []

        for file in files:
            file_changes.append({
                "filename": file.get("filename"),
                "additions": file.get("additions", 0),
                "deletions": file.get("deletions", 0),
                "changes": file.get("changes", 0)
            })

        return file_changes