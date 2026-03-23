class CommitProcessor:

    def process_commits(self, commits):

        processed = []

        for commit in commits:

            # 🔥 SAFE EXTRACTION
            commit_data = commit.get("commit") or {}
            author_data = commit_data.get("author") or {}

            # ✅ MESSAGE
            message = commit_data.get("message") or commit.get("message")
            if not message:
                message = "No commit message available"

            print("DEBUG MESSAGE:", message)

            # ✅ AUTHOR FIX (CRITICAL)
            author = author_data.get("name") or commit.get("author")

            if isinstance(author, dict):  # safety
                author = author.get("name")

            if not author:
                author = "Unknown"

            # ✅ DATE
            date = author_data.get("date") or commit.get("date")

            # ✅ URL
            url = commit.get("html_url") or commit.get("url")

            processed_commit = {
                "sha": commit.get("sha"),
                "message": message,
                "author": author,
                "date": date,
                "url": url,
                "files": commit.get("files", []),

                "type": "other",
                "type_distribution": {},
                "code_insights": []
            }

            processed.append(processed_commit)

        return processed