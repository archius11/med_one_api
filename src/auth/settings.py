
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMS_MESSAGE_TEMPLATE = 'Ваш код авторизации Med ONE: {code}'


auth_settings = Settings()
