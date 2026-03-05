# GitHub API Integration Design

GitChronicle uses the GitHub REST API to retrieve repository commit history.

The API endpoint used is:

GET /repos/{owner}/{repo}/commits

Example:

https://api.github.com/repos/openai/gpt-engineer/commits

---

## Authentication

GitHub API requests are authenticated using a Personal Access Token (PAT).

Authentication header:

Authorization: token <GITHUB_TOKEN>

This increases the API rate limit from:

60 requests/hour → 5000 requests/hour.

---

## Token Storage

Tokens are stored in a `.env` environment file to prevent exposure in the codebase.

Example:

GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx

The `.env` file is excluded from Git version control using `.gitignore`.

---

## Request Structure

Example API request:

GET https://api.github.com/repos/{owner}/{repo}/commits

Headers:

Authorization: token GITHUB_TOKEN

Accept: application/vnd.github.v3+json

---

## Response Handling

GitHub returns commit data as JSON objects.

GitChronicle processes these objects and extracts only the required fields.

---

## Why GitHub REST API

Advantages:

Simple HTTP requests

Rich repository metadata

Wide community support

Stable and well-documented

---

## Future Improvements

Pagination handling for large repositories

File-level change extraction

Commit diff analysis

Commit activity clustering