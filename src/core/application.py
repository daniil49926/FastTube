from fastapi import FastAPI
from core.service.healthchecker import healthchecker_router_v1
from apps.routers import router


_app = None


def get_app():
    global _app
    if not _app:
        _app = FastAPI(
            title="FastTube",
            version="0.0.2",
            description=""
        )

        _app.include_router(healthchecker_router_v1)
        _app.include_router(router)

    return _app


