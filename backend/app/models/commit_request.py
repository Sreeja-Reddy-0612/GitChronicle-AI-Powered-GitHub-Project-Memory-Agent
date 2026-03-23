from pydantic import BaseModel


class CommitRequest(BaseModel):
    repo_url: str
    sha: str