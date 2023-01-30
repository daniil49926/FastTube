import redis

from core.settings import settings


def get_redis_conn() -> redis.StrictRedis:

    __as_redis = redis.StrictRedis(
        username=settings.REDIS_LOGIN,
        password=settings.REDIS_PWD,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )
    try:
        __as_redis.ping()
    except redis.exceptions.ConnectionError:
        pass
    return __as_redis
