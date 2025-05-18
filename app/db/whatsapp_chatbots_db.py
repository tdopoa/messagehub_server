import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import pyodbc

from .db import Database


class WhatsAppChatBots(Database):
    def __init__(self):
        super().__init__()

    def create_chatbot(
        self,
        tenant_id: str,
        name: str,
        description: str,
        type: str,
        webhook: str,
        api_token: str,
        phone_number_id: str,
        api_url: str,
        initial_message: str,
        reject_message: str,
        completion_message: str,
    ) -> str:
        chatbot_id = str(uuid.uuid4())
        query = """
        INSERT INTO WhatsAppChatBots (
            TenantId, ChatBotId, Name, Description, Type, Webhook, ApiToken,
            PhoneNumberId, ApiURL, InitialMessage, RejectMessage, CompletionMessage
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    tenant_id,
                    chatbot_id,
                    name,
                    description,
                    type,
                    webhook,
                    api_token,
                    phone_number_id,
                    api_url,
                    initial_message,
                    reject_message,
                    completion_message,
                ),
            )
            conn.commit()
        return chatbot_id

    def update_chatbot(self, chatbot_id: str, **kwargs) -> bool:
        allowed_fields = {
            "Name",
            "Description",
            "Type",
            "Webhook",
            "ApiToken",
            "PhoneNumberId",
            "ApiURL",
            "InitialMessage",
            "RejectMessage",
            "CompletionMessage",
        }

        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not update_fields:
            return False

        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        query = f"""
        UPDATE WhatsAppChatBots 
        SET {set_clause}, UpdateAt = GETDATE()
        WHERE ChatBotId = ?
        """

        print(query)

        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*update_fields.values(), chatbot_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_chatbot(self, chatbot_id: str) -> bool:
        # First delete related records
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            # Delete answers
            cursor.execute(
                "DELETE FROM WhatsAppChatBotsAnswares WHERE ChatBotId = ?",
                (chatbot_id),
            )
            # Delete questions
            cursor.execute(
                "DELETE FROM WhatsAppChatBotsQuestions WHERE ChatBotId = ?",
                (chatbot_id),
            )
            # Delete chatbot
            cursor.execute(
                "DELETE FROM WhatsAppChatBots WHERE ChatBotId = ?",
                (chatbot_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_chatbot(self, tenant_id: str, chatbot_id: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM WhatsAppChatBots WHERE TenantId = ? AND ChatBotId = ?"
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id, chatbot_id))
            row = cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in cursor.description], row))
            return None

    def get_chatbot_by_id(self, chatbot_id: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM WhatsAppChatBots WHERE ChatBotId = ?"
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (chatbot_id))
            row = cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in cursor.description], row))
            return None

    def list_chatbots(self, tenant_id: str) -> List[Dict[str, Any]]:
        query = (
            "SELECT * FROM WhatsAppChatBots WHERE TenantId = ? ORDER BY CreateAt DESC"
        )
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id,))
            return [
                dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()
            ]

    def create_question(
        self,
        tenant_id: str,
        chatbot_id: str,
        question: str,
        order: int,
        expected_response_type: str,
        expected_response_options: str,
    ) -> str:
        question_id = str(uuid.uuid4())
        query = """
        INSERT INTO WhatsAppChatBotsQuestions (
            TenantId, ChatBotId, [ChatBotQuestionId], Question, [Order], ExpectedResponseType, ExpectedResponseOptions    
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    tenant_id,
                    chatbot_id,
                    question_id,
                    question,
                    order,
                    expected_response_type,
                    expected_response_options,
                ),
            )
            conn.commit()
        return question_id

    def update_question(
        self,
        tenant_id: str,
        chatbot_id: str,
        question_id: str,
        question: Optional[str] = None,
        order: Optional[int] = None,
        expected_response_type: Optional[str] = None,
        expected_response_options: Optional[str] = None,
    ) -> bool:
        update_fields = []
        params = []
        if question is not None:
            update_fields.append("Question = ?")
            params.append(question)
        if order is not None:
            update_fields.append("[Order] = ?")
            params.append(str(order))
        if expected_response_type is not None:
            update_fields.append("ExpectedResponseType = ?")
            params.append(expected_response_type)
        if expected_response_options is not None:
            update_fields.append("ExpectedResponseOptions = ?")
            params.append(str(expected_response_options))
        if not update_fields:
            return False

        query = f"""
        UPDATE WhatsAppChatBotsQuestions 
        SET {", ".join(update_fields)}, UpdateAt = GETDATE()
        WHERE TenantId = ? AND ChatBotId = ? AND ChatBotQuestionId = ?
        """

        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*params, tenant_id, chatbot_id, question_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_question(self, question_id: str) -> bool:
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            # Delete answers first
            cursor.execute(
                "DELETE FROM WhatsAppChatBotsAnswares WHERE ChatBotQuestionId = ?",
                (question_id),
            )
            # Delete question
            cursor.execute(
                "DELETE FROM WhatsAppChatBotsQuestions WHERE ChatBotQuestionId = ?",
                (question_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_question(
        self, tenant_id: str, chatbot_id: str, question_id: str
    ) -> Optional[Dict[str, Any]]:
        query = """
        SELECT * FROM WhatsAppChatBotsQuestions 
        WHERE TenantId = ? AND ChatBotId = ? AND ChatBotQuestionId = ?
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id, chatbot_id, question_id))
            row = cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in cursor.description], row))
            return None

    def list_questions(self, chatbot_id: str) -> List[Dict[str, Any]]:
        query = """
        SELECT * FROM WhatsAppChatBotsQuestions 
        WHERE ChatBotId = ? 
        ORDER BY [Order]
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (chatbot_id))
            return [
                dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()
            ]

    def create_answer(
        self, tenant_id: str, chatbot_id: str, question_id: str, answer: str
    ) -> str:
        answer_id = str(uuid.uuid4())
        query = """
        INSERT INTO WhatsAppChatBotsAnswares (
            TenantId, ChatBotId, ChatBotQuestionId, ChatBotAnswaresId, Answare
        ) VALUES (?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                query, (tenant_id, chatbot_id, question_id, answer_id, answer)
            )
            conn.commit()
        return answer_id

    def update_answer(
        self,
        tenant_id: str,
        chatbot_id: str,
        question_id: str,
        answer_id: str,
        answer: str,
    ) -> bool:
        query = """
        UPDATE WhatsAppChatBotsAnswares 
        SET Answare = ?, UpdateAt = GETDATE()
        WHERE TenantId = ? AND ChatBotId = ? AND ChatBotQuestionId = ? AND ChatBotAnswaresId = ?
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(
                query, (answer, tenant_id, chatbot_id, question_id, answer_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_answer(
        self, tenant_id: str, chatbot_id: str, question_id: str, answer_id: str
    ) -> bool:
        query = """
        DELETE FROM WhatsAppChatBotsAnswares 
        WHERE TenantId = ? AND ChatBotId = ? AND ChatBotQuestionId = ? AND ChatBotAnswaresId = ?
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id, chatbot_id, question_id, answer_id))
            conn.commit()
            return cursor.rowcount > 0

    def get_answer(
        self, tenant_id: str, chatbot_id: str, question_id: str, answer_id: str
    ) -> Optional[Dict[str, Any]]:
        query = """
        SELECT * FROM WhatsAppChatBotsAnswares 
        WHERE TenantId = ? AND ChatBotId = ? AND ChatBotQuestionId = ? AND ChatBotAnswaresId = ?
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id, chatbot_id, question_id, answer_id))
            row = cursor.fetchone()
            if row:
                return dict(zip([column[0] for column in cursor.description], row))
            return None

    def list_answers(
        self, tenant_id: str, chatbot_id: str, question_id: str
    ) -> List[Dict[str, Any]]:
        query = """
        SELECT * FROM WhatsAppChatBotsAnswares 
        WHERE TenantId = ? AND ChatBotId = ? AND ChatBotQuestionId = ?
        ORDER BY CreateAt
        """
        with pyodbc.connect(self._build_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tenant_id, chatbot_id, question_id))
            return [
                dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()
            ]
