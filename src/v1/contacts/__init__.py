from fastapi import APIRouter

from ..contacts.resource import contacts

api_router = APIRouter()

api_router.include_router(router=contacts.router)
