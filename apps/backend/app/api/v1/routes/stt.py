# apps/backend/app/api/v1/routes/stt.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.stt_whispercpp import transcribe_file

router = APIRouter(prefix="/api/v1/stt", tags=["stt"])

@router.post("/transcribe")
async def stt_transcribe(
    audio: UploadFile = File(..., description="Audio file (.wav/.mp3/.m4a/.ogg/.webm)"),
    language: str = Form(default="en", description="Language code (e.g., en, hi, auto)"),
):
    try:
        data = await audio.read()
        text = transcribe_file(data, language=language)
        return {"text": text, "language": language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
