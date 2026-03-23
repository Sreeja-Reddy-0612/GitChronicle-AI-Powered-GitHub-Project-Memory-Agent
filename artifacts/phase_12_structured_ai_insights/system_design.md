# GitChronicle System Design – Phase 12

Phase 12 refines the "AI Explanation" and "Frontend Visualization" modules of the GitChronicle pipeline.

---

## Refined System Flow

User → API → GitHub Data Collector → **Structured Commit Analysis** → Phase Detection → **Interactive AI Explanation** → **Premium Frontend Visualization**

---

## Components Enhanced

### 1. LLM Code Insight Engine (Backend)
-   **Input**: Git patch + retrieved context.
-   **Processing**: Multi-level prompt + JSON parsing + Sanitization.
-   **Output**: Structured object with overall and per-file insights.

### 2. GitHub Client (Backend)
-   Robust data retrieval with binary file detection and error suppression.

### 3. Commit Explanation Explorer (Frontend)
-   Interactive React page with state-driven expansion and formatted rendering.

---

## Phase 12 Deliverables

1.  **JSON Protocol**: Structured communication between backend and frontend.
2.  **Sanitized Content**: Clean, readable AI insights without markdown clutter.
3.  **Interactive UI**: Expandable file-by-file breakdown with premium styling.
4.  **Robust Backend**: Crash-proof processing for all file types and model fallbacks.

---

## Technology Updates

-   **Frontend**: React (State management for interactive items).
-   **Backend**: Python (Regex-based text post-processing).
-   **AI**: Gemini 1.5/2.0 & OpenAI GPT-4o-mini (Structured JSON mode).
