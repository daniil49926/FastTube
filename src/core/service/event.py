from fastapi import APIRouter

from core.db import database
from core.redisdb.redisdb import async_redis

event_router = APIRouter()


@event_router.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    await async_redis.connect()


@event_router.on_event("shutdown")
async def shutdown():
    await database.async_session().close()
    await database.engine.dispose()
    await async_redis.close_redis()
