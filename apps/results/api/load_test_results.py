from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.controllers.load_test_results import get_load_test_results, get_load_test_result_details, \
    crate_load_test_result
from apps.results.schema.load_test_results import GetLoadTestResultsQuery, GetLoadTestResultsResponse, \
    GetLoadTestResultDetailsResponse, CreateLoadTestResultRequest
from services.postgres.client import get_postgres_session
from utils.routes import APIRoutes

load_test_results_router = APIRouter(
    prefix=APIRoutes.LOAD_TEST_RESULTS,
    tags=[APIRoutes.LOAD_TEST_RESULTS.as_tag()]
)


@load_test_results_router.get('', response_model=GetLoadTestResultsResponse)
async def get_load_test_results_vew(
        query: Annotated[GetLoadTestResultsQuery, Depends(GetLoadTestResultsQuery.as_query)],
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_load_test_results(query, session)


@load_test_results_router.get(
    '/details/{load_test_results_id}',
    response_model=GetLoadTestResultDetailsResponse
)
async def get_load_test_result_details_view(
        load_test_results_id: int,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await get_load_test_result_details(load_test_results_id, session)


@load_test_results_router.post('', response_model=GetLoadTestResultDetailsResponse)
async def crate_load_test_result_view(
        request: CreateLoadTestResultRequest,
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return await crate_load_test_result(request, session)
