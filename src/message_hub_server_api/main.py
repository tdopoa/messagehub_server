from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from message_hub_server_api.v1 import (
    contacts,
    customers,
    profiles,
    whatsapp_chatbots,
    whatsapp_chatbots_questions,
)

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
    app.include_router(contacts.api_router, prefix="/contacts", tags=["Contacts"])
    app.include_router(profiles.api_router, prefix="/profiles", tags=["Profiles"])
    app.include_router(customers.api_router, prefix="/customers", tags=["Customers"])
    app.include_router(
        whatsapp_chatbots_questions.api_router,
        prefix="",
        tags=["WhatsApp Chatbots"],
    )
    app.include_router(
        whatsapp_chatbots.api_router,
        prefix="",
        tags=["WhatsApp Chatbots"],
    )

    @app.get("/")
    def index():
        return {"Hello": "World"}

    return app
