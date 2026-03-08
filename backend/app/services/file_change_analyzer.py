from typing import List
from app.models.commit_model import Commit
from app.services.github_client import GitHubClient


class FileChangeAnalyzer:

    def __init__(self):
        self.github_client = GitHubClient()

    def enrich_commits_with_files(self, owner: str, repo: str, commits: List[Commit]):

        for commit in commits:

            files = self.github_client.get_commit_details(
                owner,
                repo,
                commit.sha
            )

            commit.files = files

        return commits