# GitChronicle – Phase 3
## Commit Processing Engine

### Objective

The objective of Phase 3 is to convert raw GitHub commit data into structured internal objects that can be analyzed by later stages of the GitChronicle pipeline.

While Phase 2 focused on collecting commit history from the GitHub API, the data returned by the API is still raw JSON and not suitable for analysis.

Phase 3 introduces a commit processing engine that transforms this raw data into structured commit objects.

---

### Why This Phase Is Important

Raw API responses contain unnecessary metadata and inconsistent structures. For reliable analysis and future AI processing, the system needs a clean internal representation of commit data.

This phase establishes the internal data model used by GitChronicle.

---

### Key Components Introduced

Commit Data Model

File Change Data Model

Commit Processor Service

These components form the core data pipeline that converts raw GitHub commit responses into structured commit objects.

---

### Pipeline After Phase 3

Repository URL  
↓  
GitHub API Client  
↓  
Raw Commit JSON  
↓  
Commit Processor  
↓  
Structured Commit Objects

---

### Example Structured Commit
{
"sha": "009a8712166182ebc427ad7b7eb20ca9b1c1945",
"message": "Revise README for Youtube RAG QA System",
"author": "Sreeja Reddy",
"date": "2026-01-18",
"url": "https://github.com/.../commit/009a8712166182eb
",
"files": []
}

---

### Phase Result

GitChronicle now processes commit history into structured objects ready for deeper analysis.

This prepares the system for Phase 4 where file-level changes and diff analysis will be introduced.