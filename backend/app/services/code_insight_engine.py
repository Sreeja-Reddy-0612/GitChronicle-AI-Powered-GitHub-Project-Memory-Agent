class CodeInsightEngine:

    def process_commits(self, commits):

        for commit in commits:

            insights = []

            for file in commit.get("files", []):

                patch = file.get("patch", "")
                filename = file.get("filename", "")

                if not patch:
                    continue

                added, removed = [], []

                for line in patch.split("\n"):
                    if line.startswith("+") and not line.startswith("+++"):
                        added.append(line[1:].strip())
                    elif line.startswith("-") and not line.startswith("---"):
                        removed.append(line[1:].strip())

                if not added and not removed:
                    continue

                role = self._detect_role(filename)
                change = self._detect_change(added, removed)
                relation = self._detect_relation(added)

                insights.append({
                    "file": filename,
                    "role": role,
                    "change": change,
                    "relation": relation,
                    "impact": self._estimate_impact(file)
                })

            commit["code_insights"] = insights

        return commits

    def _detect_role(self, filename):

        if "frontend" in filename and ".jsx" in filename:
            return "Frontend React component"

        if "backend" in filename and "app.py" in filename:
            return "Backend API server"

        if "routes" in filename:
            return "API route handler"

        if "services" in filename:
            return "Business logic layer"

        if filename.endswith(".md"):
            return "Documentation"

        return "General file"

    def _detect_change(self, added, removed):

        if added and not removed:
            return "New functionality added"

        if removed and not added:
            return "Code removed"

        if added and removed:
            return "Existing logic modified"

        return "Minor update"

    def _detect_relation(self, added):

        text = " ".join(added)

        if "fetch(" in text or "axios" in text:
            return "Frontend connected to backend API"

        if "requests." in text:
            return "Backend calling external service"

        if "import" in text or "from" in text:
            return "New dependency introduced"

        return "Internal update"

    def _estimate_impact(self, file):

        changes = file.get("changes", 0)

        if changes > 80:
            return "high"
        elif changes > 30:
            return "medium"
        return "low"