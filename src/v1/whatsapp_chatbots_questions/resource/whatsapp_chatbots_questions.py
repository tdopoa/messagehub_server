from typing import List, Optional

from fastapi import APIRouter

from src.v1.db.whatsapp_chatbots_db import WhatsAppChatBots
from src.v1.whatsapp_chatbots.resource.whatsapp_chatbot_question_in import (
    PostWhatsAppChatBotQuestionIn,
)
from src.v1.whatsapp_chatbots.resource.whatsapp_chatbot_question_out import (
    GetWhatsAppChatBotQuestionOut,
)

router = APIRouter(prefix="")


@router.get(
    "/questions-list/{chatbot_id}", response_model=List[GetWhatsAppChatBotQuestionOut]
)
async def get_questions_list(chatbot_id: str) -> List[GetWhatsAppChatBotQuestionOut]:
    """
    Obtém a lista de perguntas de um chatbot.
    """
    questions = WhatsAppChatBots().list_questions(chatbot_id)
    return [GetWhatsAppChatBotQuestionOut(**question) for question in questions]


@router.get(
    "/questions/{chatbot_id}/{question_id}",
    response_model=GetWhatsAppChatBotQuestionOut,
)
async def get_question_by_id(
    tenant_id: str, chatbot_id: str, question_id: str
) -> Optional[GetWhatsAppChatBotQuestionOut]:
    """
    Obtém uma pergunta específica pelo ID.
    """
    question = WhatsAppChatBots().get_question(tenant_id, chatbot_id, question_id)
    if not question:
        return None
    return GetWhatsAppChatBotQuestionOut(**question)


@router.post("/questions", response_model=GetWhatsAppChatBotQuestionOut)
async def post_question(
    body: PostWhatsAppChatBotQuestionIn,
) -> Optional[GetWhatsAppChatBotQuestionOut]:
    """
    Cria uma nova pergunta.
    """
    print(body)
    question_id = WhatsAppChatBots().create_question(
        tenant_id=body.tenant_id,
        chatbot_id=body.chatbot_id,
        question=body.question,
        order=body.order,
        expected_response_type=body.expected_response_type,
        expected_response_options=body.expected_response_options,
    )
    question = WhatsAppChatBots().get_question(
        body.tenant_id, body.chatbot_id, question_id
    )
    if not question:
        return None
    return GetWhatsAppChatBotQuestionOut(**question)


@router.put(
    "/questions/{chatbot_id}/{question_id}",
    response_model=GetWhatsAppChatBotQuestionOut,
)
async def put_question(
    tenant_id: str,
    chatbot_id: str,
    question_id: str,
    body: PostWhatsAppChatBotQuestionIn,
) -> Optional[GetWhatsAppChatBotQuestionOut]:
    """
    Atualiza uma pergunta existente.
    """
    WhatsAppChatBots().update_question(
        tenant_id=tenant_id,
        chatbot_id=chatbot_id,
        question_id=question_id,
        question=body.question,
        order=body.order,
        expected_response_type=body.expected_response_type,
        expected_response_options=body.expected_response_options,
    )
    question = WhatsAppChatBots().get_question(tenant_id, chatbot_id, question_id)
    if not question:
        return None
    return GetWhatsAppChatBotQuestionOut(**question)


@router.delete("/questions/{question_id}")
async def delete_question(question_id: str):
    """
    Remove uma pergunta pelo ID.
    """
    WhatsAppChatBots().delete_question(question_id)
    return {"message": f"Pergunta com ID {question_id} removida com sucesso."}
