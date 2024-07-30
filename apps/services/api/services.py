from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.services.controllers.services import get_services
from apps.services.schema.services import GetServicesResponse
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

services_router = APIRouter(
    prefix=APIRoutes.SERVICES,
    tags=[APIRoutes.SERVICES.as_tag()]
)


@services_router.get('', response_model=GetServicesResponse)
async def get_services_view(session: Annotated[AsyncSession, Depends(get_postgres_session)]):
    return await get_services(session)
