from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io
import pyttsx3
import tempfile
import os

router = APIRouter()

@router.post("/api/v1/tts/speak")
async def speak(payload: dict):
    text = (payload or {}).get("text", "")
    if not text:
        return {"error": "text is required"}
    engine = pyttsx3.init()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        out_path = f.name
    try:
        engine.save_to_file(text, out_path)
        engine.runAndWait()
        audio = open(out_path, "rb")
        return StreamingResponse(audio, media_type="audio/wav")
    finally:
        try:
            os.remove(out_path)
        except OSError:
            pass
