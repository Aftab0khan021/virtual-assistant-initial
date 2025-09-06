from fastapi import APIRouter, UploadFile, File
from app.nlu.router import route_nlu
from app.schemas.intent import IntentRequest
from app.skills.timer import TimerSkill
from app.skills.weather import WeatherSkill
from app.skills.system_time import SystemTimeSkill
import asyncio

router = APIRouter()

@router.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    # Placeholder until whisper.cpp is wired
    _ = await audio.read()  # consume uploaded audio
    return {"text": "hello world"}

@router.post("/understand")
async def understand(payload: IntentRequest):
    """
    Runs rule-based NLU and executes mapped skills.
    Returns a friendly 'reply' string for the UI to display/speak.
    """
    resp = await route_nlu(payload)

    # TIMER (default 5s if none provided)
    if resp.intent == "timer.set":
        secs = int(resp.slots.get("seconds", 5))
        # run asynchronously; don't block the HTTP request
        asyncio.create_task(TimerSkill().run(seconds=secs))
        resp.reply = f"Okay, timer set for {secs} seconds."

    # TIME
    elif resp.intent == "system.time":
        out = await SystemTimeSkill().run()
        resp.reply = out.get("spoken", "I told the time.")

    # WEATHER (default: New Delhi coords — change as you like)
    elif resp.intent == "weather.get":
        out = await WeatherSkill().run(latitude=28.6139, longitude=77.2090)
        cw = out.get("data", {})
        temp = cw.get("temperature")
        wind = cw.get("windspeed")
        resp.reply = f"Delhi right now: {temp}°C, wind {wind} km/h."

    # GREETING demo (if your router returns intent='greeting')
    elif resp.intent == "greeting":
        resp.reply = resp.reply or "Hello! How can I help?"

    # FALLBACK
    if not resp.reply:
        resp.reply = "Sorry, I didn’t catch that."

    return resp
