from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Request, Response

from src.auth.models import User

from src.auth.dependencies import login_user_data, auth_code_confirm_login, get_current_user

from src.auth.utils import create_access_token, create_refresh_token

from src.auth.sms import SMS_Verification

jwt_auth_router = APIRouter()


@jwt_auth_router.post('/login', summary="User login")
async def login_user(
        user: User = Depends(login_user_data)
):
    SMS_Verification.send_sms_code(user)
    return user.id


@jwt_auth_router.post('/sms_confirmation', summary="Auth code")
async def sms_confirmation(
        response: Response,
        user_verification: Annotated[dict, Depends(auth_code_confirm_login)]
):
    code_is_right = SMS_Verification.check_sms_code(user_verification['current_user'],
                                                    user_verification['confirmation_code'])

    if not code_is_right:
        raise HTTPException(status_code=400, detail="Invalid code.")

    access_token = create_access_token(user_verification['current_user'].id)
    response.set_cookie("access_token", access_token, httponly=True)

    refresh_token = create_refresh_token(user_verification['current_user'].id)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return {"access_token": access_token, "refresh_token": refresh_token}


@jwt_auth_router.get('/refresh', summary="Refresh access token")
async def refresh(
        response: Response,
        user=Depends(get_current_user)
):
    access_token = create_access_token(user.id)
    response.set_cookie("access_token", access_token, httponly=True)

    return {"access_token": access_token}
