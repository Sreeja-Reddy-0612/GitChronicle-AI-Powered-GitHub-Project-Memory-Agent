from pydantic import BaseModel
from typing import List


class FileChange(BaseModel):
    filename: str
    additions: int = 0
    deletions: int = 0
    changes: int = 0


class Commit(BaseModel):
    sha: str
    message: str
    author: str
    date: str
    url: str
    files: List[FileChange] = []