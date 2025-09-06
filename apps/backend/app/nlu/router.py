from app.schemas.intent import IntentRequest, IntentResponse
from .rules import rule_match
from .llm import llm_infer

async def route_nlu(req: IntentRequest) -> IntentResponse:
    rule = rule_match(req.text)
    if rule:
        return rule
    return await llm_infer(req)
