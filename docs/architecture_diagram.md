# Orbit V1 Architecture Diagram

**Status:** Proposed architecture — draft for team review.

## Architecture Overview

```mermaid
flowchart TD
    A[Approved Public Lead Sources] --> B[Lead Generation Agent]
    B --> C[Research and Qualification]
    C --> D[(PostgreSQL Database)]
    D --> E[Human Review]
    E --> F[Outreach Drafting Agent]
    F --> G[Human Approval]
    G --> H[Approved Outreach Channel]
    H --> I[Response and Follow-up Tracking]
    I --> D
    J[n8n Workflow Orchestration] --> B
    J --> F
    J --> I
    K[FastAPI Backend] --> D
    L[Dashboard - Planned] --> K
