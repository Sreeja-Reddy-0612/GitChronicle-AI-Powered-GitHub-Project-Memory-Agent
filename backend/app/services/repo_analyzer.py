from app.services.github_client import GitHubClient
from app.services.commit_processor import CommitProcessor
from app.services.file_change_analyzer import FileChangeAnalyzer
from app.services.commit_classifier import CommitClassifier
from app.utils.repo_parser import parse_repo_url


class RepoAnalyzer:

    def __init__(self):

        self.github_client = GitHubClient()
        self.commit_processor = CommitProcessor()
        self.file_change_analyzer = FileChangeAnalyzer(self.github_client)
        self.commit_classifier = CommitClassifier()

    def analyze_repository(self, repo_url):

        owner, repo = parse_repo_url(repo_url)

        commits = self.github_client.get_commits(owner, repo)

        commits = self.commit_processor.process_commits(commits)

        commits = self.file_change_analyzer.enrich_commits(owner, repo, commits)

        commits = self.commit_classifier.classify_commits(commits)

        return {
            "repository": repo_url,
            "owner": owner,
            "repo": repo,
            "total_commits": len(commits),
            "commits": commits
        }