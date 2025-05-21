from fastapi import APIRouter

from message_hub_server_api.v1.profiles.resource import profiles

api_router = APIRouter()

api_router.include_router(router=profiles.router)
