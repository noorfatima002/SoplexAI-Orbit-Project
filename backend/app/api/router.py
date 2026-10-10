from fastapi import APIRouter, Depends

from app.api.routes import agents, companies, health, leads
from app.core.security import require_api_key

api_router = APIRouter()

# Public: liveness / readiness checks only.
api_router.include_router(health.router)

# Everything else requires the X-API-Key header.
protected = APIRouter(dependencies=[Depends(require_api_key)])
protected.include_router(companies.router)
protected.include_router(leads.router)
protected.include_router(agents.router)
api_router.include_router(protected)
