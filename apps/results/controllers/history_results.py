from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.history_results import GetHistoryResultsResponse, GetHistoryResultsQuery, HistoryResult, \
    CreateHistoryResultsRequest
from services.postgres.models import HistoryResultsModel


async def get_history_results(
        query: GetHistoryResultsQuery,
        session: AsyncSession
) -> GetHistoryResultsResponse:
    results = await HistoryResultsModel.filter(
        session,
        clause_filter=(HistoryResultsModel.load_test_results_id == query.load_test_result_id,)
    )

    return GetHistoryResultsResponse(
        results=[HistoryResult.model_validate(result) for result in results]
    )


async def create_history_results(request: CreateHistoryResultsRequest, session: AsyncSession):
    for result in request.results:
        await HistoryResultsModel.create(
            session, **result.model_dump(), load_test_results_id=request.load_test_results_id
        )
