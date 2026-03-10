# Architecture Notes – Phase 1

GitChronicle follows a modular backend architecture designed for scalability and maintainability.

The system is divided into multiple layers.

---

## Architecture Layers

### 1. API Layer

Handles incoming requests from clients.

Implemented using FastAPI.

Responsibilities:

• receive repository URLs  
• validate input data  
• trigger backend analysis pipeline  

Location:

app/routes/

---

### 2. Service Layer

Handles core business logic.

Responsibilities:

• GitHub API interaction  
• commit data retrieval  
• repository analysis  

Location:

app/services/

---

### 3. Model Layer

Defines data structures used by the system.

Responsibilities:

• request validation  
• internal data representation  

Location:

app/models/

---

### 4. Utility Layer

Contains helper functions used across modules.

Responsibilities:

• repository URL parsing  
• helper utilities  

Location:

app/utils/

---

## Design Philosophy

GitChronicle separates responsibilities between layers to ensure:

• modular design  
• easier testing  
• maintainability  
• scalability

This structure allows future components such as commit analysis and AI explanation modules to be added without affecting the API layer.