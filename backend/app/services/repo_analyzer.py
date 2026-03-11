from app.utils.repo_parser import parse_repo_url
from app.services.github_client import GitHubClient
from app.services.commit_processor import CommitProcessor
from app.services.file_change_analyzer import FileChangeAnalyzer
from app.services.commit_classifier import CommitClassifier
from app.services.repo_intelligence import RepoIntelligence
from app.services.phase_builder import PhaseBuilder


class RepoAnalyzer:

    def __init__(self):

        # Initialize GitHub client
        self.github_client = GitHubClient()

        # Other services
        self.commit_processor = CommitProcessor()

        # IMPORTANT FIX
        self.file_change_analyzer = FileChangeAnalyzer(self.github_client)

        self.commit_classifier = CommitClassifier()

        self.repo_intelligence = RepoIntelligence()

        self.phase_builder = PhaseBuilder()

    def analyze_repository(self, repo_url):

        owner, repo = parse_repo_url(repo_url)

        # Step 1: Get commits
        commits = self.github_client.get_commits(owner, repo)

        # Step 2: Process commits
        commits = self.commit_processor.process_commits(commits)

        # Step 3: Analyze file changes
        commits = self.file_change_analyzer.enrich_commits(
            owner,
            repo,
            commits
        )

        # Step 4: Classify commits
        commits = self.commit_classifier.classify_commits(commits)

        # Step 5: Generate repository insights
        insights = self.repo_intelligence.generate_insights(commits)

        phases = self.phase_builder.build_phases(commits)

        return {
            "repository": repo_url,
            "owner": owner,
            "repo": repo,
            "total_commits": len(commits),
            "commits": commits,
            "insights": insights,
            "development_phases": phases
        }