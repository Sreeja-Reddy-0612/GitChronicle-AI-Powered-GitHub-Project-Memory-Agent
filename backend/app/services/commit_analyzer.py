from app.services.github_client import GitHubClient
from app.services.llm_code_insight_engine import LLMCodeInsightEngine
from app.utils.repo_parser import parse_repo_url


class CommitAnalyzer:

    def __init__(self):
        self.github_client = GitHubClient()
        self.llm_engine = LLMCodeInsightEngine()

    def analyze_commit(self, repo_url, sha):

        owner, repo = parse_repo_url(repo_url)

        # 🔥 GET FULL COMMIT DETAILS
        data = self.github_client.get_commit_details(owner, repo, sha)

        commit_data = data.get("commit", {})
        author_data = commit_data.get("author", {})

        message = commit_data.get("message")
        author = author_data.get("name")
        date = author_data.get("date")

        files = []

        combined_patch = ""

        for f in data.get("files", []):
            filename = f.get("filename")
            patch = f.get("patch", "")

            files.append({
                "filename": filename,
                "changes": f.get("changes", 0)
            })

            if patch:
                combined_patch += f"\nFILE: {filename}\n{patch}\n"

        # 🔥 SINGLE LLM CALL
        summary = self.llm_engine.analyze_commit(owner, repo, sha, message, combined_patch)

        return {
            "sha": sha,
            "message": message,
            "author": author,
            "date": date,
            "files": files,
            "analysis": summary
        }