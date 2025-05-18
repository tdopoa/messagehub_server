from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PostWhatsAppChatBotQuestionIn(BaseModel):
    tenant_id: str = Field(alias="TenantId")
    chatbot_id: str = Field(alias="ChatBotId")
    chatbot_question_id: Optional[str] = Field(alias="ChatBotQuestionId", default=None)
    question: str = Field(alias="Question")
    order: int = Field(alias="Order")
    expected_response_type: str = Field(alias="ExpectedResponseType")
    expected_response_options: str = Field(alias="ExpectedResponseOptions")

    class Config:
        populate_by_name = True
