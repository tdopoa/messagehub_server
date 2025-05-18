from typing import List, Optional

from fastapi import APIRouter

from app.db.whatsapp_chatbots_db import WhatsAppChatBots
from v1.whatsapp_chatbots.schema.input.whatsapp_chatbot import PostWhatsAppChatBotIn
from v1.whatsapp_chatbots.schema.output.whatsapp_chatbot import GetWhatsAppChatBotOut

router = APIRouter(prefix="")


@router.get("/whatsapp-chatbots-list/", response_model=List[GetWhatsAppChatBotOut])
async def get_chatbots_list(tenant_id: str) -> List[GetWhatsAppChatBotOut]:
    """
    Obtém a lista de chatbots.
    """
    chatbots = WhatsAppChatBots().list_chatbots(tenant_id)
    return [GetWhatsAppChatBotOut(**chatbot) for chatbot in chatbots]


@router.get(
    "/whatsapp-chatbots-list-by-tenant-id/{tenant_id}",
    response_model=List[GetWhatsAppChatBotOut],
)
async def get_chatbots_list_by_tenant_id(tenant_id: str) -> List[GetWhatsAppChatBotOut]:
    """
    Obtém a lista de chatbots.
    """
    chatbots = WhatsAppChatBots().list_chatbots(tenant_id)
    return [GetWhatsAppChatBotOut(**chatbot) for chatbot in chatbots]


@router.get("/whatsapp-chatbots/{chatbot_id}", response_model=GetWhatsAppChatBotOut)
async def get_chatbot_by_id(chatbot_id: str) -> Optional[GetWhatsAppChatBotOut]:
    """
    Obtém um chatbot específico pelo ID.
    """
    chatbot = WhatsAppChatBots().get_chatbot_by_id(chatbot_id)
    if not chatbot:
        return None

    return GetWhatsAppChatBotOut(**chatbot)


@router.post("/whatsapp-chatbots", response_model=GetWhatsAppChatBotOut)
async def post_chatbot(body: PostWhatsAppChatBotIn) -> Optional[GetWhatsAppChatBotOut]:
    """
    Cria um novo chatbot.
    """
    chatbot_id = WhatsAppChatBots().create_chatbot(
        tenant_id=body.tenant_id,
        name=body.name,
        description=body.description,
        type=body.type,
        webhook=body.webhook,
        api_token=body.api_token,
        phone_number_id=body.phone_number_id,
        api_url=body.api_url,
        initial_message=body.initial_message,
        reject_message=body.reject_message,
        completion_message=body.completion_message,
    )
    chatbot = WhatsAppChatBots().get_chatbot(body.tenant_id, chatbot_id)
    if not chatbot:
        return None
    return GetWhatsAppChatBotOut(**chatbot)


@router.put("/whatsapp-chatbots/{chatbot_id}", response_model=GetWhatsAppChatBotOut)
async def put_chatbot(
    chatbot_id: str, body: PostWhatsAppChatBotIn
) -> Optional[GetWhatsAppChatBotOut]:
    """
    Atualiza um chatbot existente.
    """
    update_data = {
        "Name": body.name,
        "Description": body.description,
        "Type": body.type,
        "Webhook": body.webhook,
        "ApiToken": body.api_token,
        "PhoneNumberId": body.phone_number_id,
        "ApiURL": body.api_url,
        "InitialMessage": body.initial_message,
        "RejectMessage": body.reject_message,
        "CompletionMessage": body.completion_message,
    }
    WhatsAppChatBots().update_chatbot(chatbot_id, **update_data)
    chatbot = WhatsAppChatBots().get_chatbot_by_id(chatbot_id)
    if not chatbot:
        return None
    return GetWhatsAppChatBotOut(**chatbot)


@router.delete("/whatsapp-chatbots/{chatbot_id}")
async def delete_chatbot(chatbot_id: str):
    """
    Remove um chatbot pelo ID.
    """
    WhatsAppChatBots().delete_chatbot(chatbot_id)
    return {"message": f"Chatbot com ID {chatbot_id} removido com sucesso."}
