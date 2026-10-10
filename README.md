# SoplexAI Orbit - AI Sales Intelligence & Automation (Phase 1 setup)

Phase 1 goal: a reproducible development environment (FastAPI + PostgreSQL + n8n), a draft data model,
and documentation. The agents themselves are built in later phases.

## Prerequisites
- Git
- Docker Desktop (includes Docker Compose) - needed for the Docker route
- Python 3.12+ - only needed if you run the backend outside Docker

## Quick start (Docker - recommended)

```bash
# 1. Create your local config and EDIT the values (never commit .env)
cp .env.example .env            # Windows PowerShell: Copy-Item .env.example .env

# 2. Start PostgreSQL + backend + n8n (migrations run automatically)
docker compose up --build
```

| Service | URL |
|---|---|
| API health | http://localhost:8000/health |
| API docs (development only) | http://localhost:8000/docs |
| n8n | http://localhost:5678 |

Quick checks (the API key is `API_KEY` from your `.env`):

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health/db
curl -X POST http://localhost:8000/api/v1/companies \
  -H "X-API-Key: <your API_KEY>" -H "Content-Type: application/json" \
  -d '{"name": "Acme Digital", "website": "https://www.acme.com"}'
```

Look at the data in Postgres:

```bash
docker compose exec postgres psql -U orbit -d orbit -c "SELECT id, name, domain FROM companies;"
```

Stop: `docker compose down` (add `-v` to also delete the database volume).

## Run the backend without Docker (optional)

```bash
docker compose up -d postgres          # database only
cd backend
python -m venv .venv
source .venv/bin/activate              # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
alembic upgrade head                   # create the tables
uvicorn app.main:app --reload          # http://localhost:8000
```

## Tests

No Docker or Postgres needed - tests use an in-memory SQLite database.

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

## Database migrations

```bash
cd backend
alembic upgrade head                                   # apply
alembic revision --autogenerate -m "describe change"   # after editing app/models/entities.py
alembic downgrade -1                                   # undo the last migration
```

## Project structure

```
backend/app/api/       routes (versioned under /api/v1)
backend/app/core/      config, database, security, logging, error handling
backend/app/models/    SQLAlchemy tables (11)
backend/app/schemas/   request/response validation (Pydantic)
backend/app/services/  business logic helpers
backend/app/agents/    agent contract (agents come in later phases)
backend/alembic/       database migrations
backend/tests/         pytest tests
n8n/                   n8n notes + exported workflows
frontend/              dashboard placeholder (later phase)
docs/                  architecture, data model, security, stack and risks
```

## Security rules
- Never commit `.env`, API keys, passwords or tokens. Only `.env.example` (placeholders) is committed.
- Keep development and production configuration separate. In production the app refuses to start with placeholder secrets.
- See `docs/security_notes.md`.

## Git workflow
- `main` = stable, `dev` = integration, work in `feature/<name>` branches.
- Open a pull request into `dev`; the other team member reviews before merge. No direct pushes to `main`.

## Demo script (Phase 1 evidence)
1. `docker compose up --build`  2. open `/health`  3. POST a company  4. show the row with `psql`  5. run `pytest`
