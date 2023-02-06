import aioredis

from core.settings import settings


class __AsyncRedisClient:
    def __init__(self):
        self.__as_redis = None

    async def connect(self) -> None:
        if self.__as_redis is None:
            self.__as_redis = await aioredis.StrictRedis(
                username=settings.REDIS_LOGIN,
                password=settings.REDIS_PWD,
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
            )
        await self.__check_conn()

    async def __check_conn(self) -> None:
        try:
            await self.__as_redis.ping()
        except aioredis.exceptions.ConnectionError as e:
            print(e)

    async def get_async_redis(self):
        if self.__as_redis is None:
            await self.connect()
        return self.__as_redis

    async def close_redis(self):
        self.__as_redis.close()


async_redis = __AsyncRedisClient()
