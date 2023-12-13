from fastapi import APIRouter
from src.auth.router import auth_router


router = APIRouter(prefix="/auth")

router.include_router(router=auth_router, tags=["Authentication"])
