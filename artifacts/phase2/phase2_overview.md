# GitChronicle – Phase 2
## GitHub API Integration and Commit Collection

### Objective

The goal of Phase 2 was to integrate GitChronicle with the GitHub REST API in order to retrieve repository commit history. This enables the system to access the development activity of a project and prepare the data required for further analysis.

This phase establishes the **data ingestion pipeline** of GitChronicle.

---

### What Was Implemented

GitHub REST API integration

Personal Access Token authentication

Commit history retrieval

Commit metadata extraction

API endpoint updated to return commit information

Environment configuration for secure token management

---

### Data Retrieved From GitHub

For each commit the system extracts:

• commit SHA  
• commit message  
• commit author  
• commit timestamp  
• commit URL

This structured information becomes the foundation for the commit analysis engine implemented in later phases.

---

### Example Output
{
"sha": "8eff4fd8e1ff75619b27761c53d7df2ee963bc8b",
"message": "modify live demo section in README",
"author": "Sreeja Reddy",
"date": "2026-01-24",
"url": "https://github.com/.../commit/8eff4fd
..."
}

---

### Key Result

GitChronicle can now retrieve real development history from any GitHub repository.

This transforms the system from a static backend service into a **data-driven repository analysis engine**.

---

### Phase Status

Commit collection engine implemented successfully.
Ready for commit analysis in Phase 3.