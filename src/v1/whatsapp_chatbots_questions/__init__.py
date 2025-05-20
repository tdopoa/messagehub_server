from fastapi import APIRouter

from .resource import whatsapp_chatbot_question

api_router = APIRouter()

api_router.include_router(router=whatsapp_chatbot_question.router)
