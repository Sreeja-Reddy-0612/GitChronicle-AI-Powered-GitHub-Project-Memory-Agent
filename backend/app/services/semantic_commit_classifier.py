from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticCommitClassifier:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Semantic prototypes
        self.commit_types = {
            "feature": "implement new functionality add capability introduce system feature",
            "bugfix": "fix error resolve bug correct failure repair issue",
            "refactor": "improve structure refactor code optimization performance cleanup",
            "docs": "documentation update readme guide explanation comments",
            "test": "add test testing validation unit test coverage",
            "maintenance": "update dependencies configuration minor improvements maintenance"
        }

        self.type_embeddings = {
            key: self.model.encode(text)
            for key, text in self.commit_types.items()
        }

    def classify(self, message):

        msg_embedding = self.model.encode(message)

        best_type = "other"
        best_score = 0

        for commit_type, emb in self.type_embeddings.items():

            score = cosine_similarity([msg_embedding], [emb])[0][0]

            if score > best_score:
                best_score = score
                best_type = commit_type

        return best_type