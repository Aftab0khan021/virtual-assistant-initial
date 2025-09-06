from app.schemas.intent import IntentRequest, IntentResponse

# Placeholder: wire your preferred LLM provider with tool-calling
async def llm_infer(req: IntentRequest) -> IntentResponse:
    # naive fallback: echo
    return IntentResponse(intent="chitchat", slots={}, confidence=0.4, reply=f"You said: {req.text}")
