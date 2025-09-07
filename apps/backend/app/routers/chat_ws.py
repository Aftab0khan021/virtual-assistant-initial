from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from urllib.parse import parse_qs, urlparse
from datetime import datetime
from app.db import get_session
from app.models import Message

router = APIRouter()

def small_brain(user_text: str) -> str:
    t = user_text.strip().lower()
    if t in {"hi","hello","hey"}: return "Hello! How can I help you?"
    if "time" in t: return datetime.now().strftime("The time is %I:%M %p")
    if "date" in t: return datetime.now().strftime("Today is %A, %d %B %Y")
    return f"You said: {user_text}"

@router.websocket("/ws/chat")
async def chat_ws(ws: WebSocket):
    parsed = urlparse(str(ws.url))
    session_id = parse_qs(parsed.query).get("session_id", ["default"])[0]
    await ws.accept()
    try:
        while True:
            user_text = await ws.receive_text()
            with get_session() as s:
                s.add(Message(session_id=session_id, role="user", content=user_text)); s.commit()
            reply = small_brain(user_text)
            with get_session() as s:
                s.add(Message(session_id=session_id, role="assistant", content=reply)); s.commit()
            await ws.send_text(reply)
    except WebSocketDisconnect:
        return
