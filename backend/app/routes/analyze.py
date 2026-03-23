from fastapi import APIRouter
from app.models.repo_request import RepoRequest
from app.models.commit_request import CommitRequest
from app.services.repo_analyzer import RepoAnalyzer
from app.services.commit_analyzer import CommitAnalyzer

router = APIRouter()

repo_analyzer = RepoAnalyzer()
commit_analyzer = CommitAnalyzer()


@router.post("/analyze-repo")
def analyze_repo(request: RepoRequest):
    return repo_analyzer.analyze_repository(request.repo_url)


@router.post("/analyze-commit")
def analyze_commit(request: CommitRequest):

    return commit_analyzer.analyze_commit(
        request.repo_url,
        request.sha
    )