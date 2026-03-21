class CommitProcessor:

    def process_commits(self, commits):

        processed = []

        for commit in commits:

            # ✅ NOW DIRECTLY FROM CLIENT OUTPUT
            message = commit.get("message")
            author = commit.get("author")
            date = commit.get("date")
            url = commit.get("url")

            # 🔥 FALLBACK SAFETY
            if not message:
                message = "No commit message available"

            if not author:
                author = "Unknown"

            print("DEBUG MESSAGE:", message)

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