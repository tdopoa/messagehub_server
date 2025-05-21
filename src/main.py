from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.v1.contacts.resource import contacts
from src.v1.customers.resource import customers
from src.v1.profiles.resource import profiles
from src.v1.whatsapp_chatbots.resource import whatsapp_chatbot
from src.v1.whatsapp_chatbots_questions.resource import whatsapp_chatbot_question

app = FastAPI()

load_dotenv()


def create_app():
    app = FastAPI(title="Message HUB API", version="1.0.0")

    origins = [
        "http://localhost:4200",  # A origem do seu frontend Angular
        # Adicione outras origens conforme necessário (ex: para produção)
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
    app.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
    app.include_router(customers.router, prefix="/customers", tags=["Customers"])
    app.include_router(
        whatsapp_chatbot_question.router,
        prefix="",
        tags=["WhatsApp Chatbots"],
    )
    app.include_router(
        whatsapp_chatbot.router,
        prefix="",
        tags=["WhatsApp Chatbots"],
    )

    @app.get("/")
    def index():
        return {"Hello": "World"}

    return app
