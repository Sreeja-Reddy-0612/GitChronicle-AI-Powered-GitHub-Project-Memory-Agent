class PhaseDetector:

    def __init__(self):
        pass

    def detect_phase(self, commit_type):

        if commit_type == "feature":
            return "Feature Development"

        if commit_type == "fix":
            return "Bug Fixing"

        if commit_type == "refactor":
            return "Code Refactoring"

        if commit_type == "docs":
            return "Documentation"

        return "Maintenance"