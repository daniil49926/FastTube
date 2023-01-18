from fastapi import APIRouter

from apps.auth.views import v1 as auth_v1
from apps.player.views import v1 as player_v1
from apps.user.views import v1 as user_v1
from apps.video.views import v1 as video_v1

router = APIRouter()

router.include_router(user_v1, prefix="/user/v1", tags=["user"])
router.include_router(video_v1, prefix="/video/v1", tags=["video"])
router.include_router(auth_v1, tags=["auth"])
router.include_router(player_v1, prefix="/player/v1", tags=["player"])
