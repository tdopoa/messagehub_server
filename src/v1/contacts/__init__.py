from fastapi import APIRouter

from v1.contacts.resource import contacts

api_router = APIRouter()

api_router.include_router(router=contacts.router)
