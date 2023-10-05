from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Request

from src.auth.models import User

from src.auth.dependencies import login_user_data, auth_code_confirm_login


jwt_auth_router = APIRouter()


@jwt_auth_router.post('/login', summary="User login")
async def login_user(
        user: User = Depends(login_user_data)
):

    # user = db.get(data.email, None)
    # if user is not None:
    #         raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="User with this email already exist"
    #     )
    # user = {
    #     'email': data.email,
    #     'password': get_hashed_password(data.password),
    #     'id': str(uuid4())
    # }
    # db[data.email] = user    # saving user to database

    # create auth_code
    # "1111"
    return user.id


@jwt_auth_router.post('/sms_confirmation', summary="Auth code")
async def sms_confirmation(
        user_verification: Annotated[dict, Depends(auth_code_confirm_login)]
):
    if not user_verification['confirmation_code'] == user_verification['sent_code']:
        raise HTTPException(status_code=400, detail="Invalid code.")

    return user_verification
