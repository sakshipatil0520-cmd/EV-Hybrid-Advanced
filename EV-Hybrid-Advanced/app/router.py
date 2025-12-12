from fastapi import APIRouter
from .auth import router as auth_router
from .predict_router import router as predict_router

router = APIRouter()
router.include_router(auth_router, prefix="")
router.include_router(predict_router, prefix="")
