from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.routers import router as apps_router
from core.middleware.analytics import AnalyticsMiddleware
from core.middleware.logger import LoggerMiddleware
from core.middleware.time_process import TimedProcessMiddleware
from core.service.routers import router as core_router
from core.utils.configure_logger import configure_and_get_logger

_app = None


def get_app():
    global _app
    if not _app:
        _app = FastAPI(title="FastTube", version="0.0.2", description="")
        _app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
        )
        _app.add_middleware(TimedProcessMiddleware)
        _app.add_middleware(AnalyticsMiddleware)
        _app.add_middleware(LoggerMiddleware, logger=configure_and_get_logger())
        _app.include_router(core_router)
        _app.include_router(apps_router)

    return _app
