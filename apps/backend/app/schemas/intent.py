from pydantic import BaseModel

class IntentRequest(BaseModel):
    text: str
    locale: str = "en-IN"
    context: dict | None = None

class IntentResponse(BaseModel):
    intent: str
    slots: dict = {}
    confidence: float = 0.0
    reply: str | None = None
