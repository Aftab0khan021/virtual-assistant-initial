from fastapi import APIRouter, UploadFile, File, HTTPException
from faster_whisper import WhisperModel
import tempfile
import os

router = APIRouter()
_model = WhisperModel("base", device="cpu")  # change to "cuda" if you have GPU

@router.post("/api/v1/stt/transcribe")
async def transcribe(file: UploadFile = File(...), language: str = "en"):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    suffix = os.path.splitext(file.filename)[1].lower() or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        segments, info = _model.transcribe(tmp_path, language=language)
        text = "".join(seg.text for seg in segments).strip()
        return {"text": text, "language": info.language, "language_probability": info.language_probability}
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
