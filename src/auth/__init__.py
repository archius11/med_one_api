from fastapi import APIRouter
from src.auth.jwt import jwt_auth_router


auth_router = APIRouter(prefix="/auth")

auth_router.include_router(router=jwt_auth_router, tags=["JWT Authentication"])
