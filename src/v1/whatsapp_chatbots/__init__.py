from fastapi import APIRouter

from v1.whatsapp_chatbots.resource import whatsapp_chatbot
from v1.whatsapp_chatbots_questions.resource import whatsapp_chatbot_question

api_router = APIRouter()

api_router.include_router(router=whatsapp_chatbot.router)
api_router.include_router(router=whatsapp_chatbot_question.router)
