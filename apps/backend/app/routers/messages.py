from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.db import get_session
from app.models import Message

router = APIRouter()

@router.get("/api/v1/messages", response_model=List[Message])
def list_messages(session_id: str = Query(...), limit: int = 100):
    with get_session() as s:
        stmt = select(Message).where(Message.session_id == session_id).order_by(Message.created_at.asc()).limit(limit)
        rows = s.exec(stmt).all()
        return rows

@router.delete("/api/v1/messages/clear")
def clear_messages(session_id: str = Query(...)):
    with get_session() as s:
        rows = s.exec(select(Message).where(Message.session_id == session_id)).all()
        for r in rows:
            s.delete(r)
        s.commit()
        return {"deleted": len(rows)}
