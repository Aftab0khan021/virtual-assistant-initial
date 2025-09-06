# apps/backend/app/api/v1/__init__.py
from fastapi import APIRouter
from . import voice, skills
from . import tts  # <-- add this

router = APIRouter()
router.include_router(voice.router, prefix="/voice", tags=["voice"])
router.include_router(skills.router, prefix="/skills", tags=["skills"])
router.include_router(tts.router, prefix="/tts", tags=["tts"])  # <-- add this
