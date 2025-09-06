# apps/backend/app/api/v1/tts.py
from fastapi import APIRouter
from pydantic import BaseModel
import threading
from app.tts.pyttsx_engine import speak

router = APIRouter()

class SpeakIn(BaseModel):
    text: str

@router.post("/speak")
def tts_speak(payload: SpeakIn):
    # run TTS in a background thread so the API returns quickly
    threading.Thread(target=speak, args=(payload.text,), daemon=True).start()
    return {"ok": True}
