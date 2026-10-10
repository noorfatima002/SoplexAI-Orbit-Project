# Orbit V1 - Architecture (draft)

```mermaid
flowchart LR
    U[Authorized team member] --> D[Dashboard - Next.js, later phase]
    D -->|X-API-Key / login| API[FastAPI backend /api/v1]
    N8N[n8n workflows - schedules and triggers] -->|HTTP + X-API-Key| API
    API --> DB[(PostgreSQL)]
    subgraph Agents [Specialist agents - Python, later phases]
      LG[Lead Generation]
      OA[Outreach]
      FA[Follow-up]
      RA[Response / Sales]
    end
    API -->|queues job_runs| Agents
    Agents -->|read / write| DB
    Agents -->|model calls| LLM[AI model provider]
    OA -.->|draft only| AP{Human approval}
    AP -->|approved_by set| SEND[Sending - email / LinkedIn / Upwork]
```

## Boundaries
- **n8n** only schedules and triggers; it calls the backend API and holds no business data.
- **FastAPI** is the single entry point for data changes, validation, access control and audit logging.
- **Agents** never talk to each other; they communicate only through PostgreSQL rows (`leads.status`, `job_runs`, ...).
- **Nothing is sent without human approval** (enforced in the database: approved/sent messages need `approved_by`).
- Every agent checks `opt_outs` before preparing or sending anything.

## Failure handling
- `job_runs` stores status, `attempt`, `max_attempts`, `error_message`; failed jobs go to `retrying` until max attempts, then `failed`.
- `idempotency_key` makes repeated triggers safe (same key returns the same job).
- Duplicates: `companies.domain` is unique; `contacts` unique per `(company_id, email)`.
