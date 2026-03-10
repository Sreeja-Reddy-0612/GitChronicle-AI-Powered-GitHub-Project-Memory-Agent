import requests
import os


class GitHubClient:

    def __init__(self):

        token = os.getenv("GITHUB_TOKEN")

        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }

    def get_commits(self, owner, repo):

        url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=10"

        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.text}")

        return response.json()

    def get_commit_details(self, owner, repo, sha):

        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"

        response = requests.get(url, headers=self.headers, timeout=10)

        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.text}")

        return response.json()