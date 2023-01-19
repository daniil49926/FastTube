from builtins import object
from fastapi import Depends, APIRouter
from core.db import database
from core.db.database import get_db

event_router = APIRouter()


@event_router.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


@event_router.on_event("shutdown")
async def shutdown(session: object = Depends(get_db)):
    await session.close()
    await database.engine.dispose()
