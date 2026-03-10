# Data Model Design – Commit Objects

GitChronicle uses structured data models to represent repository activity.

These models define how commit data is stored internally.

---

## Commit Model

The Commit model represents a single repository commit.

Fields:

sha  
message  
author  
date  
url  
files

---

## Commit Object Example
Commit(
sha="abc123",
message="add authentication module",
author="John Doe",
date="2026-01-10",
url="https://github.com/repo/commit/abc123
",
files=[]
)


---

## FileChange Model

The FileChange model represents file modifications inside a commit.

Fields:

filename  
additions  
deletions  
changes  

Example:


FileChange(
filename="auth.py",
additions=120,
deletions=10,
changes=130
)


---

## Why Data Models Matter

Using data models ensures that the system processes consistent and validated data structures.

Advantages include:

Type validation

Structured analysis

Cleaner code

Better debugging

Easier extension for future features