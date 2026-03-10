# Implementation Notes – Phase 2

During Phase 2 the GitHub API client module was implemented.

The following development steps were completed.

---

## Step 1 – Environment Configuration

A `.env` file was created to store the GitHub Personal Access Token.

This allows secure authentication when making API requests.

---

## Step 2 – GitHub Client Service

The GitHub client module was implemented inside:

app/services/github_client.py

This module handles communication with the GitHub REST API.

---

## Step 3 – Commit Retrieval

The following API endpoint was used:

GET /repos/{owner}/{repo}/commits

The response was parsed and essential commit metadata was extracted.

---

## Step 4 – API Endpoint Update

The `/analyze-repo` endpoint was updated to return commit history for the requested repository.

---

## Result

GitChronicle can now retrieve real commit data from GitHub repositories.

This enables future modules to perform commit analysis and project evolution detection.