class FileChangeAnalyzer:

    def __init__(self, github_client):
        self.github_client = github_client

    def enrich_commits(self, owner, repo, commits):

        enriched = []

        for commit in commits:

            sha = commit["sha"]

            details = self.github_client.get_commit_details(owner, repo, sha)

            files = []

            if "files" in details:

                for file in details["files"]:

                    files.append({
                        "filename": file.get("filename"),
                        "additions": file.get("additions"),
                        "deletions": file.get("deletions"),
                        "changes": file.get("changes")
                    })

            commit["files"] = files

            enriched.append(commit)

        return enriched