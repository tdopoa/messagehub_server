from fastapi import APIRouter

from .resource import customers

api_router = APIRouter()

api_router.include_router(router=customers.router)
