from collections import defaultdict
from app.services.phase_detector import PhaseDetector


class PhaseBuilder:

    def __init__(self):
        self.detector = PhaseDetector()

    def build_phases(self, commits):

        phases = defaultdict(list)

        for commit in commits:

            commit_type = commit.get("type", "other")

            phase = self.detector.detect_phase(commit_type)

            phases[phase].append(commit)

        phase_list = []

        index = 1

        for phase_name, commits in phases.items():

            phase_list.append({
                "phase_number": index,
                "phase_name": phase_name,
                "commit_count": len(commits),
                "commits": commits
            })

            index += 1

        return phase_list