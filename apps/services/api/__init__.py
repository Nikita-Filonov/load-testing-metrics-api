from fastapi import APIRouter

from apps.services.api.services import services_router

services_app_router = APIRouter()
services_app_router.include_router(services_router)
