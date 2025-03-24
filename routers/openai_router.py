from fastapi import APIRouter
from services.openai_agent import chat_with_openai
from models.openai import Prompt

router = APIRouter()

@router.post("/chat")
def chat_endpoint(prompt: Prompt):
    result = chat_with_openai(prompt.prompt)
    return {"response": result}