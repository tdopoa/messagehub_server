from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseWhatsAppChatBot(BaseModel):
    tenant_id: str = Field(alias="TenantId")
    chatbot_id: str = Field(alias="ChatBotId")
    name: str = Field(alias="Name")
    description: str = Field(alias="Description")
    type: str = Field(alias="Type")
    webhook: str = Field(alias="Webhook")
    api_token: str = Field(alias="ApiToken")
    phone_number_id: str = Field(alias="PhoneNumberId")
    api_url: str = Field(alias="ApiURL")
    initial_message: str = Field(alias="InitialMessage")
    reject_message: str = Field(alias="RejectMessage")
    completion_message: str = Field(alias="CompletionMessage")
    create_at: Optional[datetime] = Field(alias="CreateAt", default=None)
    update_at: Optional[datetime] = Field(alias="UpdateAt", default=None)

    class Config:
        populate_by_name = True


class WhatsAppChatBotQuestion(BaseModel):
    tenant_id: str = Field(alias="TenantId")
    chatbot_id: str = Field(alias="ChatBotId")
    chatbot_question_id: str = Field(alias="ChatBotQuestionId")
    expected_response_type: str = Field(alias="ExpectedResponseType")
    expected_response_options: list[str] = Field(alias="ExpectedResponseOptions")
    question: str = Field(alias="Question")
    order: int = Field(alias="Order")
    create_at: Optional[datetime] = Field(alias="CreateAt", default=None)
    update_at: Optional[datetime] = Field(alias="UpdateAt", default=None)

    class Config:
        populate_by_name = True


class WhatsAppChatBotAnswer(BaseModel):
    tenant_id: str = Field(alias="TenantId")
    chatbot_id: str = Field(alias="ChatBotId")
    chatbot_question_id: str = Field(alias="ChatBotQuestionId")
    chatbot_answer_id: str = Field(alias="ChatBotAnswaresId")
    answer: str = Field(alias="Answare")
    create_at: Optional[datetime] = Field(alias="CreateAt", default=None)
    update_at: Optional[datetime] = Field(alias="UpdateAt", default=None)

    class Config:
        populate_by_name = True
