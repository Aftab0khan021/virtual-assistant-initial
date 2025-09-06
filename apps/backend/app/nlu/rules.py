# apps/backend/app/nlu/rules.py
from app.schemas.intent import IntentResponse

RULES = [
    (("set","timer"), "timer.set"),
    (("start","timer"), "timer.set"),
    (("weather",), "weather.get"),
    (("what","time"), "system.time"),   # <-- already had this idea
    (("time",), "system.time"),         # <-- add a looser match
]

def rule_match(text: str) -> IntentResponse | None:
    t = text.lower()
    for keywords, intent in RULES:
        if all(k in t for k in keywords):
            return IntentResponse(intent=intent, slots={}, confidence=0.8, reply=None)
    return None
