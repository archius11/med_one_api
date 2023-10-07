import redis.asyncio as redis

from src.settings import settings

from src.redis.settings import redis_settings


class RedisClient:
    REDIS_POOL = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    REDIS_CLIENT = redis.Redis(connection_pool=REDIS_POOL)

    @classmethod
    async def ping(cls):
        await cls.REDIS_CLIENT.ping()

    @classmethod
    async def set_key(cls, key, value, expire: int = redis_settings.REDIS_DEFAULT_EXPIRE_SEC):
        await cls.REDIS_CLIENT.set(key, value)
        await cls.REDIS_CLIENT.expire(key, expire)

    @classmethod
    async def get_key(cls, key):
        return await cls.REDIS_CLIENT.get(key)

    @classmethod
    async def set_dict(cls, key, value, expire: int = redis_settings.REDIS_DEFAULT_EXPIRE_SEC):
        await cls.REDIS_CLIENT.hset(name=key, mapping=value)
        await cls.REDIS_CLIENT.expire(key, expire)

    @classmethod
    async def set_dict_key(cls, key, dict_key, value, expire: int = redis_settings.REDIS_DEFAULT_EXPIRE_SEC):
        await cls.REDIS_CLIENT.hset(name=key, key=dict_key, value=value)
        await cls.REDIS_CLIENT.expire(key, expire)

    @classmethod
    async def get_dict(cls, key):
        return await cls.REDIS_CLIENT.hgetall(key)

    @classmethod
    async def get_dict_value(cls, key, dict_key):
        return await cls.REDIS_CLIENT.hget(key, dict_key)

    @classmethod
    async def del_key(cls, key):
        return await cls.REDIS_CLIENT.delete(key)
