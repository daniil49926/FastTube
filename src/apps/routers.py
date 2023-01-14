from fastapi import APIRouter

from apps.user.views import v1 as user_v1
from apps.video.views import v1 as video_v1

router = APIRouter()

router.include_router(user_v1, prefix="/user/v1", tags=["user"])
router.include_router(video_v1, prefix="/video/v1", tags=["video"])
