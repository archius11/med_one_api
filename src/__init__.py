from fastapi import APIRouter
from src.auth import auth_router


root = APIRouter()
root.include_router(router=auth_router, prefix="/auth")
