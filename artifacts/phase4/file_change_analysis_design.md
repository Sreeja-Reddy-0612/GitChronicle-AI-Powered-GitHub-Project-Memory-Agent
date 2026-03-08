# File Change Analysis Design

## Overview

The FileChangeAnalyzer service enriches commits with file-level change information.

Pipeline:

Repository URL
      ↓
GitHub API
      ↓
Commit Collector
      ↓
Commit Processor
      ↓
File Change Analyzer
      ↓
Structured Commit Data

## Responsibilities

The analyzer performs:

1. Fetch commit detail from GitHub
2. Extract modified files
3. Capture additions/deletions statistics
4. Attach file change data to commit objects

## Data Structure

FileChange

filename
additions
deletions
changes

Commit

sha
message
author
date
files[]

## Benefits

This design enables GitChronicle to:

- analyze which modules evolve most
- detect large refactoring commits
- track code growth patterns