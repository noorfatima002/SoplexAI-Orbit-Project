# n8n

n8n runs from docker-compose (http://localhost:5678). Exported workflows go in `n8n/workflows/`.

Calling the backend from an n8n "HTTP Request" node:
- URL: `http://backend:8000/api/v1/health` (service name `backend`, not localhost)
- Header: `X-API-Key` = the value of `API_KEY` from your `.env`
- Store the key in an n8n Credential, never hard-code it in a workflow.
