from fastapi import APIRouter

from v1.customers.resource import customers

api_router = APIRouter()

api_router.include_router(router=customers.router)
