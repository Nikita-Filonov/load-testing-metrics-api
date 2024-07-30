from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.methods import get_methods, get_method_details
from apps.results.schema.methods import GetMethodsQuery, GetMethodsResponse, GetMethodDetailsQuery, \
    GetMethodDetailsResponse
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

methods_router = APIRouter(
    prefix=APIRoutes.METHODS,
    tags=[APIRoutes.METHODS.as_tag()]
)


@methods_router.get('', response_model=GetMethodsResponse)
async def get_methods_view(
        query: Annotated[GetMethodsQuery, Depends(GetMethodsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_methods(query, session)


@methods_router.get('/details', response_model=GetMethodDetailsResponse)
async def get_method_details_view(
        query: Annotated[GetMethodDetailsQuery, Depends(GetMethodDetailsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_method_details(query, session)
