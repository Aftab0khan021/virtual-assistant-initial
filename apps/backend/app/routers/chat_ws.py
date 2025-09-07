from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from urllib.parse import parse_qs, urlparse
from datetime import datetime
from app.db import get_session
from app.models import Message

router = APIRouter()

def small_brain(user_text: str) -> str:
    t = user_text.strip().lower()
    if t in {"hi","hello","hey"}:
        return "Hello! How can I help you?"
    if t.startswith("time") or "time" in t:
        return datetime.now().strftime("The time is %I:%M %p")
    if t.startswith("date") or "date" in t:
        return datetime.now().strftime("Today is %A, %d %B %Y")
    return f"You said: {user_text}"

@router.websocket("/ws/chat")
async def chat_ws(ws: WebSocket):
    # extract session_id from query string (?session_id=xxxx)
    parsed = urlparse(str(ws.url))
    q = parse_qs(parsed.query)
    session_id = (q.get("session_id",[None])[0]) or "default"
    await ws.accept()
    try:
        while True:
            user_text = await ws.receive_text()

            # store user message
            with get_session() as s:
                s.add(Message(session_id=session_id, role="user", content=user_text))
                s.commit()

            # generate reply
            reply = small_brain(user_text)

            # store assistant message
            with get_session() as s:
                s.add(Message(session_id=session_id, role="assistant", content=reply))
                s.commit()

            # send back to this client
            await ws.send_text(reply)
    except WebSocketDisconnect:
        return
