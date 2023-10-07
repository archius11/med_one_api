import redis.asyncio as redis

from src.settings import settings


class RedisClient:
    REDIS_POOL = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    REDIS_CLIENT = redis.Redis(connection_pool=REDIS_POOL)

    @classmethod
    def ping(cls):
        cls.REDIS_CLIENT.ping()

    @classmethod
    def set_key(cls, key, value):
        cls.REDIS_CLIENT.set(key, value)

    @classmethod
    def get_key(cls, key):
        return cls.REDIS_CLIENT.get(key)
