
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMS_MESSAGE_TEMPLATE: str = 'Ваш код авторизации Med ONE: {code}'
    SMS_EXPIRE_SEC: int = 60 * 10   # 10 min
    SMS_RESEND_MIN_DELTA: int = 60  # 1 min


auth_settings = Settings()
