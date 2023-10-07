from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from src.settings import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password, )


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_PRIVATE_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt


def create_access_token(subject: Union[str, Any]) -> str:
    return create_token(subject, settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_refresh_token(subject: Union[str, Any]) -> str:
    return create_token(subject, settings.REFRESH_TOKEN_EXPIRE_MINUTES)


def normalize_phone_number(phone_number):
    return '7' + ''.join(list(filter(lambda x: x.isdigit(), phone_number))[-10:])
