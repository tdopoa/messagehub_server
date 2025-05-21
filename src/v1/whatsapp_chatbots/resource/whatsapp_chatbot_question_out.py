from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GetWhatsAppChatBotQuestionOut(BaseModel):
    tenant_id: str = Field(alias="TenantId")
    chatbot_id: str = Field(alias="ChatBotId")
    chatbot_question_id: str = Field(alias="ChatBotQuestionId")
    question: str = Field(alias="Question")
    order: int = Field(alias="Order")
    expected_response_type: str = Field(alias="ExpectedResponseType")
    expected_response_options: str = Field(alias="ExpectedResponseOptions")
    create_at: datetime = Field(alias="CreateAt")
    update_at: Optional[datetime] = Field(alias="UpdateAt", default=None)

    class Config:
        populate_by_name = True
