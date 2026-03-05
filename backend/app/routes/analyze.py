from fastapi import APIRouter
from app.models.repo_request import RepoRequest
from app.utils.repo_parser import parse_repo_url
from app.services.github_client import GitHubClient

router = APIRouter()

github_client = GitHubClient()


@router.post("/analyze-repo")
def analyze_repository(request: RepoRequest):

    owner, repo = parse_repo_url(request.repo_url)

    commits = github_client.get_commits(owner, repo)

    return {
        "repository": request.repo_url,
        "owner": owner,
        "repo": repo,
        "total_commits_fetched": len(commits),
        "commits": commits
    }