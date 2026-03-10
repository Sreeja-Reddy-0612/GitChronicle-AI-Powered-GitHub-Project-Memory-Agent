# Commit Classification Pipeline

GitChronicle repository analysis now follows this pipeline.

Step 1  
Repository URL parsing

Step 2  
GitHub API integration

Step 3  
Commit metadata extraction

Step 4  
File change analysis

Step 5  
Commit classification

The classification step enhances each commit with a development activity type.

This information enables higher-level analytics such as:

- development phase detection
- feature growth analysis
- bug fixing cycles
- refactoring trends

The classification module is implemented as a service layer and is integrated within the RepoAnalyzer orchestration pipeline.