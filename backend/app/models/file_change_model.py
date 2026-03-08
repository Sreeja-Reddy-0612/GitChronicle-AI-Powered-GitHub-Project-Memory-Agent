from pydantic import BaseModel


class FileChangeModel(BaseModel):
    filename: str
    additions: int
    deletions: int
    changes: int