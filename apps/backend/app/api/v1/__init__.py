# apps/backend/app/api/v1/__init__.py
from fastapi import APIRouter
from . import skills # 1. REMOVED 'voice'
from . import tts

router = APIRouter()
# 2. REMOVED router.include_router(voice.router, prefix="/voice", tags=["voice"])
router.include_router(skills.router, prefix="/skills", tags=["skills"])
router.include_router(tts.router, prefix="/tts", tags=["tts"])