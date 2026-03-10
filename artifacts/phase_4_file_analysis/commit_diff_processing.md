# Commit Diff Processing

## Purpose

Commit diffs contain detailed information about how the code changed between commits.

GitChronicle processes this information to understand repository evolution.

## Extracted Fields

From GitHub commit details API:

filename
additions
deletions
changes

Example response:

{
  "filename": "auth.py",
  "additions": 120,
  "deletions": 10,
  "changes": 130
}

## Processing Flow

1. Retrieve commit list
2. For each commit:
   - request commit detail
   - extract file changes
3. Attach file changes to commit object

## Output

Commit object enriched with file modification data.