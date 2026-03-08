from fastapi import APIRouter
from app.models.repo_request import RepoRequest
from app.utils.repo_parser import parse_repo_url
from app.services.github_client import GitHubClient
from app.services.commit_processor import CommitProcessor

router = APIRouter()

github_client = GitHubClient()
commit_processor = CommitProcessor()


@router.post("/analyze-repo")
def analyze_repository(request: RepoRequest):

    owner, repo = parse_repo_url(request.repo_url)

    raw_commits = github_client.get_commits(owner, repo)

    processed_commits = commit_processor.process_commits(raw_commits)

    return {
        "repository": request.repo_url,
        "owner": owner,
        "repo": repo,
        "total_commits": len(processed_commits),
        "commits": processed_commits
    }