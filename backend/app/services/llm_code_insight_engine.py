class LLMCodeInsightEngine:

    def process_commits(self, commits):

        for commit in commits:

            insights = []

            for file in commit.get("files", []):

                filename = file.get("filename")
                patch = file.get("patch", "")

                if not patch:
                    continue

                try:
                    summary = self._call_llm(filename, patch)

                except Exception as e:
                    print("LLM ERROR:", e)

                    # 🔥 FALLBACK (IMPORTANT)
                    summary = self._fallback_summary(filename, patch)

                insights.append({
                    "file": filename,
                    "summary": summary
                })

            commit["code_insights"] = insights

        return commits


    def _fallback_summary(self, filename, patch):

        if ".jsx" in filename or ".js" in filename:
            return "Frontend logic updated or UI component modified"

        if ".py" in filename:
            return "Backend logic or API functionality updated"

        if ".md" in filename:
            return "Documentation updated"

        return "Code changes applied in this file"