# Architecture Notes – Phase 12

Phase 12 introduced significant architectural refinements to the data flow between the AI engine and the frontend.

---

## Architectural Enhancements

### 1. Structured Data Protocol
Shifted from raw string-based LLM responses to a structured JSON protocol. This allows for precise mapping of AI insights to specific repository files.

**Data Structure:**
```json
{
  "overall_summary": "...",
  "file_insights": {
    "filename": "insight..."
  }
}
```

### 2. Sanitization Layer
Introduced a post-processing layer in the `LLMCodeInsightEngine` to sanitize LLM output before it reaches the frontend. This layer handles:
-   Markdown marker removal (`##`, `*`).
-   Structural bolding of headings.
-   JSON validation and parsing.

### 3. Fail-Safe Mechanisms
Improved the robustness of the system with:
-   **Binary File Handling**: Preventing encoding crashes when processing non-text files.
-   **Model Fallback Pipeline**: Sequential attempts across multiple Gemini/OpenAI models to ensure high availability.

### 4. Logic/UI Decoupling
The frontend now consumes pre-processed, structured data, allowing the UI to remain lean while providing complex interactive features like the expandable file explorer.

---

## Design Philosophy

The Phase 12 architecture prioritizes **clarity**, **interactivity**, and **robustness**, ensuring that AI insights are always readable and accessible, even in complex or multi-file commits.
