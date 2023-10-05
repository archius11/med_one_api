from typing import Optional
from fastapi import Request
from fastapi import APIRouter, HTTPException, Depends

from src.auth.schemas import LoginUserSchema, ConfirmCodeSchema
from src.auth.models import User
from src.auth.dao import UserDAO


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
        'confirmation_code': user_verification.confirmation_code,
        'sent_code': get_sent_code(user_verification.phone_number)
    }
