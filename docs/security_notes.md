# Security notes (draft for review)

| Area | Phase 1 decision | Later |
|---|---|---|
| Secrets | `.env` only, git-ignored; `.env.example` has placeholders; production refuses placeholder secrets | Secret manager on the server |
| API access | Every `/api/v1` route except health needs the `X-API-Key` header (constant-time comparison) | User login + roles (admin/member) |
| Database | Separate DB user per environment; Postgres port bound to 127.0.0.1 only | Least-privilege app user, backups, SSL |
| Audit | `audit_log` table; company creation already logged | Log every approval, send, opt-out |
| Outbound messages | Human approval enforced by a database CHECK constraint | Approval UI in dashboard |
| Opt-outs | `opt_outs` table; agents must check it first | Auto-handle "unsubscribe" replies |
| Transport | HTTPS required on orbit.soplexai.com (reverse proxy / TLS) | HSTS |
| API docs | Disabled when `APP_ENV=production` | - |
| Containers | Backend runs as non-root user | Image scanning |
| Logging | Never log keys, passwords or full message bodies | Central log storage |

Rotate any key that was ever committed or shared, even once.
