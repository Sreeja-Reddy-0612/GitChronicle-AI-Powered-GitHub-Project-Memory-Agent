# Phase 4 – File Change Analysis

## Objective
Enhance GitChronicle to analyze file-level modifications within each commit.

Until Phase 3, the system only collected commit metadata such as:
- SHA
- message
- author
- date

Phase 4 introduces deeper repository insights by retrieving the list of files modified in each commit.

## Key Capability Added
GitChronicle now extracts:

- filename
- additions
- deletions
- total changes

Example:

commit: add authentication module

files:
auth.py        +120  -10
user.py        +80   -20

## GitHub API Used

GET /repos/{owner}/{repo}/commits/{sha}

This endpoint returns detailed commit information including file changes.

## Result

Each commit object now includes a "files" field containing all modified files.

This enables future phases to analyze:

- code evolution
- module growth
- refactoring activity
- development velocity