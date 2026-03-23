import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# We use a singleton-like lazy loader for the model to save memory
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        try:
            _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            import warnings
            warnings.warn("Network unavailable. Loading Vector Store model from local cache.")
            _embedding_model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)
    return _embedding_model

class JSONVectorStore:
    def __init__(self):
        self.temp_dir = os.path.join(os.getcwd(), "temp_data")
        os.makedirs(self.temp_dir, exist_ok=True)

    def _get_db_path(self, owner, repo):
        return os.path.join(self.temp_dir, f"{owner}_{repo}_vectordb.json")

    def _chunk_text(self, text, chunk_size=800, overlap=100):
        chunks = []
        if not text:
            return chunks
        
        lines = text.split('\n')
        current_chunk = ""
        
        for line in lines:
            if len(current_chunk) + len(line) < chunk_size:
                current_chunk += line + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line + "\n"
                
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

    def build_and_save(self, owner, repo, detailed_commits):
        db_path = self._get_db_path(owner, repo)
        
        print(f"\n--- Building Knowledge Base for {owner}/{repo} ---")
        
        all_data = [] # List of dicts: {"text": ..., "sha": ...}
        
        # Extract all patches from all commits
        for commit in detailed_commits:
            commit_sha = commit.get("sha", "")
            commit_message = commit.get("message", "Unknown Commit").split('\n')[0]
            files = commit.get("files", [])
            commit_chunks_count = 0

            for f in files:
                filename = f.get("filename", "")
                patch = f.get("patch", "")
                full_content = f.get("full_content", "")
                
                # Use full content if available, otherwise fallback to patch
                content_to_chunk = full_content if full_content else patch
                
                if content_to_chunk:
                    # Prepend filename and SHA for better context
                    context_line = f"File: {filename}\nCommit SHA: {commit_sha}\n"
                    if not full_content: context_line += "(Showing Diffs Only)\n"
                    
                    file_chunks = self._chunk_text(context_line + content_to_chunk)
                    for chunk in file_chunks:
                        all_data.append({
                            "text": chunk,
                            "sha": commit_sha,
                            "filename": filename
                        })
                        commit_chunks_count += 1
            
            # User requested terminal log
            if commit_chunks_count > 0:
                print(f"Version '{commit_message}' ({commit_sha[:7]}): Created {commit_chunks_count} chunks.")

        if not all_data:
            print("No code changes found to build knowledge base.")
            return

        model = get_embedding_model()
        
        texts = [item["text"] for item in all_data]
        print(f"Generating embeddings for {len(texts)} total chunks...")
        embeddings = model.encode(texts)

        db_data = {
            "items": all_data,
            "embeddings": embeddings.tolist()
        }

        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(db_data, f)
            
        print(f"Successfully saved Knowledge Base to {db_path}\n")

    def search(self, owner, repo, query, sha=None, top_k=5):
        db_path = self._get_db_path(owner, repo)
        if not os.path.exists(db_path):
            return []
            
        with open(db_path, "r", encoding="utf-8") as f:
            db_data = json.load(f)
            
        items = db_data.get("items", [])
        embeddings = np.array(db_data.get("embeddings", []))
        
        if not items or len(embeddings) == 0:
            return []

        # If SHA is provided, prioritize or filter chunks from that commit
        if sha:
            # We filter indices where item["sha"] == sha
            indices = [i for i, item in enumerate(items) if item.get("sha") == sha]
            if indices:
                # If we have chunks for this specific commit, we use them
                filtered_items = [items[i] for i in indices]
                filtered_embeddings = embeddings[indices]
                
                # Perform search on filtered set
                model = get_embedding_model()
                query_embedding = model.encode([query])[0]
                
                norm_query = np.linalg.norm(query_embedding)
                norm_db = np.linalg.norm(filtered_embeddings, axis=1)
                norm_db[norm_db == 0] = 1e-10
                if norm_query == 0: norm_query = 1e-10
                
                similarities = np.dot(filtered_embeddings, query_embedding) / (norm_db * norm_query)
                
                k = min(top_k, len(filtered_items))
                top_indices = np.argsort(similarities)[-k:][::-1]
                return [filtered_items[i]["text"] for i in top_indices]

        # General search fallback
        model = get_embedding_model()
        query_embedding = model.encode([query])[0]
        
        norm_query = np.linalg.norm(query_embedding)
        norm_db = np.linalg.norm(embeddings, axis=1)
        norm_db[norm_db == 0] = 1e-10
        if norm_query == 0: norm_query = 1e-10
            
        similarities = np.dot(embeddings, query_embedding) / (norm_db * norm_query)
        
        k = min(top_k, len(items))
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        return [items[i]["text"] for i in top_indices]
