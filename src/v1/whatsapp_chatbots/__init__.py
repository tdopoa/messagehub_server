from fastapi import APIRouter

from src.v1.whatsapp_chatbots.resource import whatsapp_chatbot

api_router = APIRouter()

api_router.include_router(router=whatsapp_chatbot.router)
