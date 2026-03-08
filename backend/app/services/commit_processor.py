from typing import List
from app.models.commit_model import Commit


class CommitProcessor:

    def __init__(self):
        pass

    def process_commits(self, raw_commits: List[dict]) -> List[Commit]:
        """
        Convert raw GitHub commits into structured Commit objects
        """

        processed = []

        for commit in raw_commits:

            commit_obj = Commit(
                sha=commit.get("sha"),
                message=commit.get("message"),
                author=commit.get("author"),
                date=commit.get("date"),
                url=commit.get("url"),
                files=[]
            )

            processed.append(commit_obj)

        return processed