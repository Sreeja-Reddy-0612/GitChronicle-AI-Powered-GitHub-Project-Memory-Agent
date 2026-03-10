from collections import defaultdict


class RepoIntelligence:

    def generate_insights(self, commits):

        developer_activity = defaultdict(int)
        file_modifications = defaultdict(int)
        commit_type_distribution = defaultdict(int)

        largest_commit = None
        largest_changes = 0

        for commit in commits:

            author = commit.get("author", "unknown")
            developer_activity[author] += 1

            commit_type = commit.get("type", "other")
            commit_type_distribution[commit_type] += 1

            files = commit.get("files", [])

            total_changes = 0

            for file in files:

                filename = file.get("filename")
                changes = file.get("changes", 0)

                if filename:
                    file_modifications[filename] += changes

                total_changes += changes

            if total_changes > largest_changes:
                largest_changes = total_changes
                largest_commit = commit

        most_active_developer = None
        if developer_activity:
            most_active_developer = max(
                developer_activity,
                key=developer_activity.get
            )

        most_modified_files = sorted(
            file_modifications.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {

            "most_active_developer": most_active_developer,

            "developer_commit_counts": dict(developer_activity),

            "commit_type_distribution": dict(commit_type_distribution),

            "most_modified_files": [
                {"filename": f, "changes": c}
                for f, c in most_modified_files
            ],

            "largest_commit": largest_commit
        }