from fastapi import APIRouter

from core.service.healthchecker import healthchecker_router_v1
from core.service.player import v1 as player_v1

router = APIRouter()

router.include_router(
    healthchecker_router_v1, prefix="/healthchecker/v1", tags=["healthchecker"]
)
router.include_router(player_v1, prefix="/player/v1", tags=["player"])
