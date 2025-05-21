from fastapi import APIRouter

from .resource import contacts

api_router = APIRouter()

api_router.include_router(router=contacts.router)
