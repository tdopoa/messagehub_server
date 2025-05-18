from typing import Optional
from uuid import UUID

from v1.whatsapp_chatbots.schema.schema import BaseWhatsAppChatBot


class PostWhatsAppChatBotIn(BaseWhatsAppChatBot):
    chatbot_id: str = ""
