from fastapi import APIRouter

from core.service.event import event_router
from core.service.healthchecker import healthchecker_router_v1

router = APIRouter()

router.include_router(
    healthchecker_router_v1, prefix="/healthchecker/v1", tags=["healthchecker"]
)
router.include_router(event_router)
