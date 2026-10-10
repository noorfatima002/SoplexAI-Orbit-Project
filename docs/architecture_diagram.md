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
```

## System Boundaries

* **Lead Generation Agent:** Discovers, researches, qualifies, scores, and prioritizes prospects.
* **Outreach Agent:** Prepares personalized outreach drafts using company research.
* **Follow-up and Response:** Tracks interactions, classifies responses, and respects replies and opt-outs.
* **n8n:** Coordinates scheduled and event-driven workflows.
* **FastAPI:** Provides backend API endpoints for application functionality.
* **PostgreSQL:** Stores shared prospect and sales-pipeline data.
* **Dashboard:** Planned interface for authorized team members to review and monitor sales activities.
* **Human Approval:** Outreach must be reviewed and approved before it is sent.

## Important Note

This diagram represents the proposed Orbit V1 architecture for Phase 1 review. It does not mean that every agent or dashboard feature has already been implemented. The architecture and integrations should be reviewed and approved before further development.
