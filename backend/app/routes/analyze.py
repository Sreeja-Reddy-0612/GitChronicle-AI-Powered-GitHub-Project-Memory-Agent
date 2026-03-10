from fastapi import APIRouter
from app.models.repo_request import RepoRequest
from app.services.repo_analyzer import RepoAnalyzer

router = APIRouter()

analyzer = RepoAnalyzer()


@router.post("/analyze-repo")
def analyze_repo(request: RepoRequest):
    result = analyzer.analyze_repository(request.repo_url)
    return result