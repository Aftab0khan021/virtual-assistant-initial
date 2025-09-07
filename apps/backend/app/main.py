from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routers.chat_ws import router as chat_ws_router
from app.routers.stt import router as stt_router
from app.routers.tts import router as tts_router
from app.routers.messages import router as messages_router

app = FastAPI(title="Virtual Assistant API")

# Allow local UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _on_startup():
    # ensure ./data exists and create tables
    import os
    os.makedirs("./data", exist_ok=True)
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

# REST + WS routers
app.include_router(stt_router)
app.include_router(tts_router)
app.include_router(messages_router)
app.include_router(chat_ws_router)
