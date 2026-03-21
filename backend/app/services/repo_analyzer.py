from app.utils.repo_parser import parse_repo_url
from app.services.github_client import GitHubClient
from app.services.commit_processor import CommitProcessor
from app.services.semantic_commit_classifier import SemanticCommitClassifier
from app.services.repo_intelligence import RepoIntelligence
from app.services.phase_builder import PhaseBuilder
from app.services.llm_code_insight_engine import LLMCodeInsightEngine


class RepoAnalyzer:

    def __init__(self):

        self.github_client = GitHubClient()
        self.commit_processor = CommitProcessor()
        self.commit_classifier = SemanticCommitClassifier()

        # 🔥 PHASE 12
        self.code_insight_engine = LLMCodeInsightEngine()

        self.repo_intelligence = RepoIntelligence()
        self.phase_builder = PhaseBuilder()

    def _attach_patch_data(self, owner, repo, commits):
        import requests

        for commit in commits:
            sha = commit.get("sha")
            if not sha:
                continue

            url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
            res = requests.get(url, headers=self.github_client.headers)

            if res.status_code != 200:
                print("❌ Failed to fetch commit:", sha)
                continue

            data = res.json()
            files = []

            for f in data.get("files", []):
                patch = f.get("patch", "")

                # 🔥 DEBUG PATCH
                if patch:
                    print("PATCH SAMPLE:", patch[:100])

                files.append({
                    "filename": f.get("filename"),
                    "patch": patch,
                    "changes": f.get("changes", 0)
                })

            commit["files"] = files

        return commits

    def analyze_repository(self, repo_url):

        owner, repo = parse_repo_url(repo_url)

        # 1. Fetch commits
        commits = self.github_client.get_commits(owner, repo)

        # 2. Attach patch FIRST (CRITICAL)
        commits = self._attach_patch_data(owner, repo, commits)

        # 3. Process commits (extract message, author)
        commits = self.commit_processor.process_commits(commits)

        # 4. Classify commits
        commits = self.commit_classifier.classify_commits(commits)

        # 5. 🔥 Phase 12 LLM Insights
        commits = self.code_insight_engine.process_commits(commits)

        # 6. Remove patch (optional, AFTER LLM)
        for commit in commits:
            for file in commit.get("files", []):
                file.pop("patch", None)

        # 7. Repo insights
        insights = self.repo_intelligence.generate_insights(commits)

        # 8. Phases
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