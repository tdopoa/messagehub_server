from fastapi import APIRouter

from message_hub_server_api.v1.whatsapp_chatbots_questions.resource import (
    whatsapp_chatbot_question,
)

api_router = APIRouter()

api_router.include_router(router=whatsapp_chatbot_question.router)

api_router.include_router(router=whatsapp_chatbot_question.router)
