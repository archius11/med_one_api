from typing import Optional
from fastapi import Request
from fastapi import APIRouter, HTTPException, Depends

from jose import jwt, ExpiredSignatureError, JWTError

from src.auth.schemas import LoginUserSchema, ConfirmCodeSchema
from src.auth.models import User
from src.auth.dao import UserDAO
from src.auth.exceptions import TokenAbsentException, TokenExpiredException, \
    IncorrectTokenFormatException, UserIsNotPresentException

from src.settings import settings


async def get_or_create_user_by_phone(phone_number):
    current_user = await UserDAO.get_or_none(phone_number=phone_number)
    if not current_user:
        await UserDAO.create(phone_number=phone_number)
        current_user = await UserDAO.get_or_none(phone_number=phone_number)
    return current_user


async def login_user_data(request: Request, user_data: LoginUserSchema):
    current_user = await get_or_create_user_by_phone(user_data.phone_number)
    return current_user


def get_sent_code(phone_number: str) -> Optional[str]:
    return phone_number[:4]


async def auth_code_confirm_login(user_verification: ConfirmCodeSchema):
    return {
        'current_user': await get_or_create_user_by_phone(user_verification.phone_number),
        'confirmation_code': user_verification.confirmation_code
    }


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.JWT_PRIVATE_KEY, settings.JWT_ALGORITHM
        )
    except ExpiredSignatureError:
        # Как позже выяснилось, ключ exp автоматически проверяется
        # командой jwt.decode, поэтому отдельно проверять это не нужно
        raise TokenExpiredException
    except JWTError as e:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.get_by_id(user_id)
    if not user:
        raise UserIsNotPresentException

    return user
