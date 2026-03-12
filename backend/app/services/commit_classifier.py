from app.services.semantic_commit_classifier import SemanticCommitClassifier


class CommitClassifier:

    def __init__(self):

        self.semantic_classifier = SemanticCommitClassifier()

    def classify_commits(self, commits):

        for commit in commits:

            message = commit["message"]

            commit_type = self.semantic_classifier.classify(message)

            commit["type"] = commit_type

        return commits