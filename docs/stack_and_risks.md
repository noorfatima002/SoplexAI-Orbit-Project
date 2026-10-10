# Stack notes, risks and costs - backend sections (draft)

## Stack changes proposed vs the brief
| Area | Proposal | Reason |
|---|---|---|
| ORM / migrations | Add SQLAlchemy 2 + Alembic | Versioned schema changes, safer than raw SQL files |
| Validation | Pydantic v2 (comes with FastAPI) | Validates all input |
| DB driver | psycopg 3 | Current, maintained driver |
| Tests | pytest + httpx | Fast API tests; SQLite in-memory for unit tests |
| Docker | Yes, from day one | One command gives the same setup on every machine |
| Deferred | Voice, mobile, vector search, advanced orchestration | Not needed for the first milestone |

## Risks
| Risk | Mitigation |
|---|---|
| LinkedIn / Upwork terms restrict scraping and automated outreach | V1 prepares drafts only; manual sending; review terms before any integration |
| US email law (CAN-SPAM): opt-out, honest sender info | `opt_outs` table, mandatory unsubscribe handling, human approval |
| Wrong or duplicate data | Unique domain, normalization, `job_runs` idempotency |
| LLM cost and quality | Provider-agnostic wrapper, cache research, cap per-day usage |
| Leaked secrets | `.gitignore`, `.env.example`, key rotation, no secrets in logs |
| Scaling to 250 prospects/day | Queue via `job_runs`, batch work, indexes already included |

## Cost drivers (fill in real prices before submitting)
Hosting for orbit.soplexai.com (VPS), managed PostgreSQL or backups, LLM API usage, email-finding/enrichment API,
email sending infrastructure, domain/SSL, n8n (self-hosted is free; cloud is paid).
