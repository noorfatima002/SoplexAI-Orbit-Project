import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logging_config import setup_logging

logger = logging.getLogger("orbit")


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)

    # API docs are disabled in production.
    docs = None if settings.is_production else "/docs"
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url=docs,
        redoc_url=None,
        openapi_url=None if settings.is_production else "/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["X-API-Key", "Content-Type"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        logger.info(
            "%s %s -> %s (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            (time.perf_counter() - start) * 1000,
        )
        return response

    register_exception_handlers(app)
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    def home() -> dict[str, str]:
        return {"message": "SoplexAI Orbit API is running"}

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "healthy"}

    return app


app = create_app()
