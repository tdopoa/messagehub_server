from fastapi import APIRouter

from .resource import profiles

api_router = APIRouter()

api_router.include_router(router=profiles.router)
