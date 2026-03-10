class CommitClassifier:

    def classify_commits(self, commits):

        for commit in commits:

            message = commit["message"].lower()

            if "fix" in message or "bug" in message:
                commit["type"] = "bugfix"

            elif "feat" in message or "add" in message:
                commit["type"] = "feature"

            elif "refactor" in message:
                commit["type"] = "refactor"

            elif "readme" in message or "docs" in message:
                commit["type"] = "documentation"

            else:
                commit["type"] = "other"

        return commits