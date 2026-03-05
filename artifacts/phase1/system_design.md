# GitChronicle System Design – Phase 1

GitChronicle is designed as a pipeline-based system that converts GitHub repository activity into structured explanations of project evolution.

The system architecture follows a layered design.

---

## High-Level System Flow

User → API → GitHub Data Collector → Commit Analysis → Phase Detection → AI Explanation → Frontend Visualization

---

## Phase 1 Scope

Phase 1 implements only the initial part of this pipeline.

User → API → Repository Parsing → Response

---

## Components Implemented

1. FastAPI server
2. Analyze repository endpoint
3. Repository URL parser
4. GitHub client service skeleton

---

## Future Components

The following modules will be implemented in later phases.

Commit Data Processor

Commit Classification Engine

Project Evolution Detection

AI Explanation Generator

Frontend Visualization

---

## Technology Stack

Backend Framework: FastAPI

Language: Python

Dependency Management: pip

Environment Isolation: Python Virtual Environment