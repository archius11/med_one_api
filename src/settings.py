from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')

    MODE: str = Field(default='DEV')

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMS_SERVICE_HOST: str
    SMS_SERVICE_API_KEY: str
    SMS_ACCOUNT_EMAIL: str
    SMS_SENDER: str

    JWT_ALGORITHM: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    CLIENT_ORIGIN: str

    CREDENTIALS_PRIVATE_KEY: str


settings = Settings(_env_file='.env')
