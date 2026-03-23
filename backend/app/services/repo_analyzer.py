from app.utils.repo_parser import parse_repo_url
from app.services.github_client import GitHubClient
from app.services.commit_processor import CommitProcessor
from app.services.semantic_commit_classifier import SemanticCommitClassifier
from app.services.repo_intelligence import RepoIntelligence
from app.services.phase_builder import PhaseBuilder
from app.utils.vector_store import JSONVectorStore
import concurrent.futures


class RepoAnalyzer:

    def __init__(self):

        self.github_client = GitHubClient()
        self.commit_processor = CommitProcessor()
        self.commit_classifier = SemanticCommitClassifier()

        self.repo_intelligence = RepoIntelligence()
        self.phase_builder = PhaseBuilder()

    def analyze_repository(self, repo_url):

        owner, repo = parse_repo_url(repo_url)

        raw_commits = self.github_client.get_commits(owner, repo)

        def fetch_commit_details(c):
            sha = c.get("sha")
            try:
                details = self.github_client.get_commit_details(owner, repo, sha)
                files = details.get("files", [])
                
                # Enrich each file with its FULL content at this commit
                enriched_files = []
                for f in files:
                    filename = f.get("filename")
                    # We fetch the full content using the SHA as ref
                    full_content = self.github_client.get_file_content(owner, repo, filename, ref=sha)
                    enriched_files.append({
                        "filename": filename,
                        "patch": f.get("patch", ""),
                        "changes": f.get("changes", 0),
                        "full_content": full_content
                    })
                c["files"] = enriched_files
            except Exception as e:
                print(f"Error fetching details for commit {sha[:7]}: {e}")
            return c

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            detailed_commits = list(executor.map(fetch_commit_details, raw_commits))

        commits = self.commit_processor.process_commits(detailed_commits)
        
        # Build Vector DB in background (safely catch errors)
        try:
            vector_db = JSONVectorStore()
            vector_db.build_and_save(owner, repo, detailed_commits)
        except Exception as e:
            print(f"Failed to build Vector DB: {e}")

        commits = self.commit_classifier.classify_commits(commits)

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