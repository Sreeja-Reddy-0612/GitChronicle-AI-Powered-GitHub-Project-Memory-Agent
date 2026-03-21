from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SemanticCommitClassifier:

    def __init__(self):
        # Load embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Categories with better coverage (IMPORTANT)
        self.categories = {
            "feature": [
                "add new feature",
                "implement functionality",
                "create API",
                "build component",
                "develop module",
                "add system",
                "introduce feature"
            ],
            "bugfix": [
                "fix bug",
                "resolve issue",
                "fix error",
                "handle exception",
                "correct behavior",
                "patch bug"
            ],
            "refactor": [
                "refactor code",
                "improve structure",
                "clean code",
                "reorganize project",
                "remove duplication"
            ],
            "docs": [
                "update documentation",
                "add README",
                "write docs",
                "improve comments",
                "documentation update"
            ],
            "test": [
                "add tests",
                "fix test",
                "increase coverage",
                "write unit tests"
            ],
            "optimization": [
                "improve performance",
                "optimize code",
                "reduce latency",
                "speed up execution"
            ],
            "chore": [   # 🔥 VERY IMPORTANT ADDITION
                "update dependencies",
                "setup config",
                "configure environment",
                "maintenance task",
                "project setup",
                "deployment config",
                "change settings"
            ]
        }

        # Precompute category embeddings
        self.category_embeddings = self._encode_categories()

    def _encode_categories(self):
        embeddings = {}

        for category, examples in self.categories.items():
            emb = self.model.encode(examples)
            embeddings[category] = np.mean(emb, axis=0)

        return embeddings

    def _preprocess_message(self, message: str) -> str:
        """
        Extract meaningful part from commit message
        """
        if not message:
            return ""

        # Take only first line (important fix)
        message = message.split("\n")[0]

        # Lowercase
        message = message.lower()

        return message

    def classify(self, message):
        """
        Returns:
        primary_category (str)
        filtered_scores (dict)  -> multi-label output
        """

        message = self._preprocess_message(message)

        if not message:
            return "other", {}

        message_embedding = self.model.encode([message])[0]

        scores = {}

        # Compute similarity with each category
        for category, cat_embedding in self.category_embeddings.items():
            score = cosine_similarity(
                [message_embedding],
                [cat_embedding]
            )[0][0]

            scores[category] = float(score)

        # Sort by score
        sorted_scores = dict(
            sorted(scores.items(), key=lambda x: x[1], reverse=True)
        )

        # 🔥 Dynamic threshold (BEST FIX)
        max_score = max(sorted_scores.values())

        filtered_scores = {
            k: round(v, 3)
            for k, v in sorted_scores.items()
            if v >= max_score * 0.7   # relative filtering
        }

        # 🔥 Fallback (prevents empty {})
        if not filtered_scores:
            top_category = list(sorted_scores.keys())[0]
            filtered_scores = {
                top_category: round(sorted_scores[top_category], 3)
            }

        primary_category = list(filtered_scores.keys())[0]

        return primary_category, filtered_scores

    def classify_commits(self, commits):
        """
        Apply classification to list of commits
        """

        for commit in commits:
            message = commit.get("message", "")

            primary, scores = self.classify(message)

            commit["type"] = primary
            commit["type_distribution"] = scores

        return commits