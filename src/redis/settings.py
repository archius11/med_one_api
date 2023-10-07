
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_DEFAULT_EXPIRE_SEC: int = 604800  # 1 week


redis_settings = Settings()
