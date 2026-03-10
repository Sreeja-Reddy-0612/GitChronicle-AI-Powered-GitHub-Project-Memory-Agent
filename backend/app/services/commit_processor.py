class CommitProcessor:

    def process_commits(self, commits):

        processed = []

        for commit in commits:

            data = {
                "sha": commit.get("sha"),
                "message": commit.get("commit", {}).get("message"),
                "author": commit.get("commit", {}).get("author", {}).get("name"),
                "date": commit.get("commit", {}).get("author", {}).get("date"),
                "url": commit.get("html_url")
            }

            processed.append(data)

        return processed