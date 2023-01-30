import redis

from core.settings import settings

__as_redis = None


def get_redis_conn() -> redis.StrictRedis:

    global __as_redis
    if __as_redis:
        return __as_redis
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
