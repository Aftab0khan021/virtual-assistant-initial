# apps/backend/app/routers/chat_ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from urllib.parse import parse_qs, urlparse
from datetime import datetime
from app.db import get_session
from app.models import Message
from app.nlu.router import route_nlu  # <-- 1. IMPORT THE NLU ROUTER
from app.api.v1.skills import run_skill # <-- 2. IMPORT THE SKILL RUNNER
from app.schemas.intent import IntentRequest # <-- 3. IMPORT THE REQUEST SCHEMA


router = APIRouter()

# REMOVE/REPLACE THE small_brain FUNCTION

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

            # --- 4. REPLACE THIS ---
            # reply = small_brain(user_text)
            
            # --- WITH THIS ---
            # Call the powerful NLU router
            req = IntentRequest(text=user_text)
            resp = await route_nlu(req)

            # If the NLU found an intent (like 'timer.set' or 'system.open_app')
            if resp.intent != "chitchat" and resp.reply is None:
                try:
                    # Run the skill (e.g., OpenApplicationSkill)
                    skill_result = await run_skill(resp.intent, resp.slots)
                    reply = skill_result.get("spoken", "I performed the action.")
                except Exception as e:
                    reply = f"Sorry, I failed to run that skill: {str(e)}"
            else:
                # Otherwise, use the reply from the LLM (e.g., "Hello! How are you?")
                reply = resp.reply or "I'm not sure what to say."
            # --- END OF REPLACEMENT ---

            with get_session() as s:
                s.add(Message(session_id=session_id, role="assistant", content=reply)); s.commit()
            await ws.send_text(reply)
    except WebSocketDisconnect:
        return