# apps/backend/app/nlu/llm.py

from app.schemas.intent import IntentRequest, IntentResponse
from app.api.v1.skills import manifests # Import your skill manifests
from app.core.config import settings # Import settings to get the API key
import httpx, json

# Placeholder: wire your preferred LLM provider with tool-calling
async def llm_infer(req: IntentRequest) -> IntentResponse:
    
    # 1. Get all available skills to send to the LLM
    skill_manifests = await manifests()
    
    # 2. Call the LLM (Example using OpenAI)
    if settings.OPENAI_API_KEY:
        messages = [
            {"role": "system", "content": "You are a helpful assistant. You can use tools to answer user requests."},
            {"role": "user", "content": req.text}
        ]
        
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o", # or gpt-3.5-turbo
                    "messages": messages,
                    "tools": [{"type": "function", "function": m} for m in skill_manifests],
                    "tool_choice": "auto"
                }
            )
            res.raise_for_status() # Check for errors
            response_json = res.json()
            message = response_json["choices"][0]["message"]

            # 3. Check if the LLM wants to use a skill (a "tool call")
            if message.get("tool_calls"):
                tool_call = message["tool_calls"][0]
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])
                
                # Return an "Intent" to run this skill
                return IntentResponse(
                    intent=tool_name, 
                    slots=tool_args, 
                    confidence=0.9, 
                    reply=None # No reply yet, the skill will provide it
                )
            
            # 4. If no tool, just return the LLM's text reply
            return IntentResponse(
                intent="chitchat", 
                slots={}, 
                confidence=0.7, 
                reply=message.get("content", "Sorry, I'm not sure.")
            )

    # Fallback if no API key is set
    return IntentResponse(intent="chitchat", slots={}, confidence=0.4, reply=f"You said: {req.text}")