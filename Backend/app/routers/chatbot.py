from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/query", response_model=ChatResponse)
def chatbot_query(request: ChatRequest):
    msg = request.message.lower()
    if "route" in msg:
        reply = "I suggest taking the fastest route avoiding traffic."
    elif "petrol" in msg:
        reply = "Check /petrol/nearby for stations near you."
    else:
        reply = "I can help you find routes or nearby petrol stations."
    return {"reply": reply}
