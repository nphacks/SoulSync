from fastapi import APIRouter
from fastapi import Request
from pydantic import BaseModel
from typing import Optional
from utils.cosmos.journal_entry import search_vector_embeddings
from utils.azure.chatbot import build_prompt, ask_openai

class ChatRequest(BaseModel):
    user_id: str
    user_message: str
    conversation: Optional[list] = None   # Format: [{"role": "user|assistant", "content": "text"}, ...]

router = APIRouter()

@router.post("/chat/")
async def post_chat_response(chat_data: ChatRequest):

    print('Visiting chat')
    context = search_vector_embeddings(chat_data.user_id, chat_data.user_message)

    prompt = build_prompt(chat_data.user_message, context)

    response = ask_openai(prompt)
    print(response)

    # Process the chat
    return {
        "response": response,
        "user_id": chat_data.user_id,
        "history": chat_data.conversation
    }