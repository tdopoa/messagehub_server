from fastapi import APIRouter

from ..whatsapp_chatbots_questions.resource import whatsapp_chatbot_question
from .resource import whatsapp_chatbot

api_router = APIRouter()

api_router.include_router(router=whatsapp_chatbot.router)
api_router.include_router(router=whatsapp_chatbot_question.router)
