from fastapi import APIRouter
from app.models.repo_request import RepoRequest
from app.utils.repo_parser import parse_repo_url
from app.services.github_client import GitHubClient

router = APIRouter()

github_client = GitHubClient()

@router.post("/analyze-repo")
def analyze_repository(request: RepoRequest):

    owner, repo = parse_repo_url(request.repo_url)

    result = github_client.test_connection(owner, repo)

    return {
        "repository": request.repo_url,
        "parsed_owner": owner,
        "parsed_repo": repo,
        "status": result["status"]
    }