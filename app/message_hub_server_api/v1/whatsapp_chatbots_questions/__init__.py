from fastapi import APIRouter

from message_hub_server_api.v1.whatsapp_chatbots_questions.resource import (
    whatsapp_chatbots_questions,
)

api_router = APIRouter()

api_router.include_router(router=whatsapp_chatbots_questions.router)
