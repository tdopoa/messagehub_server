from typing import Optional
from uuid import UUID

from message_hub_server_api.v1.whatsapp_chatbots.resource.base_whatsapp_chatbot import (
    BaseWhatsAppChatBot,
)


class PostWhatsAppChatBotIn(BaseWhatsAppChatBot):
    chatbot_id: str = ""
