from fastapi import APIRouter

from .user.router import router as admin_user_router

router = APIRouter()
router.include_router(admin_user_router)
