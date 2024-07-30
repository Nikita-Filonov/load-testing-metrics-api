from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.load_test_results import GetLoadTestResultsQuery, \
    LoadTestResultDetails, GetLoadTestResultsResponse, LoadTestResult, \
    GetLoadTestResultDetailsResponse, CreateLoadTestResultRequest, LoadTestResultCompare
from services.postgres.models.load_test_results import LoadTestResultsModel


async def get_load_test_results_compares(
        results: Sequence[LoadTestResultsModel]
) -> list[LoadTestResultCompare]:
    compares: list[LoadTestResultCompare] = []
    for index, result in enumerate(results):
        compare = LoadTestResultCompare(
            current_total_requests_per_second=result.total_requests_per_second
        )

        try:
            previous_result = results[index + 1]

            compare.previous_id = previous_result.id
            compare.previous_total_requests_per_second = previous_result.total_requests_per_second
        except IndexError:
            ...

        compares.append(compare)

    return compares


def get_load_test_result_with_compare(
        result: LoadTestResultsModel,
        compare: LoadTestResultCompare
) -> LoadTestResult:
    load_test_result = LoadTestResult.model_validate(result)
    load_test_result.compare = compare

    return load_test_result


async def get_load_test_results(
        query: GetLoadTestResultsQuery,
        session: AsyncSession
) -> GetLoadTestResultsResponse:
    results = await LoadTestResultsModel.filter(
        session,
        limit=query.limit + 1,
        offset=query.offset,
        order_by=(LoadTestResultsModel.created_at.desc(),),
        clause_filter=(LoadTestResultsModel.service == query.service,)
    )
    total_results = await LoadTestResultsModel.count(
        session,
        column=LoadTestResultsModel.id,
        clause_filter=(LoadTestResultsModel.service == query.service,)
    )

    compares = await get_load_test_results_compares(results)

    if len(results) == query.limit + 1:
        results = results[:-1]

    return GetLoadTestResultsResponse(
        items=[
            get_load_test_result_with_compare(result, compares[index])
            for index, result in enumerate(results)
        ],
        total=total_results,
        limit=query.limit,
        offset=query.offset
    )


async def get_load_test_result_details(
        load_test_results_id: int,
        session: AsyncSession
) -> GetLoadTestResultDetailsResponse:
    result = await LoadTestResultsModel.get(
        session,
        clause_filter=(LoadTestResultsModel.id == load_test_results_id,)
    )

    previous_result = await LoadTestResultsModel.filter(
        session,
        limit=1,
        order_by=(LoadTestResultsModel.id.desc(),),
        clause_filter=(
            LoadTestResultsModel.id < load_test_results_id,
            LoadTestResultsModel.service == result.service
        )
    )

    details = LoadTestResultDetails.model_validate(result)
    if len(previous_result) > 0:
        details.compare = LoadTestResultCompare(
            previous_id=previous_result[0].id,
            current_total_requests_per_second=result.total_requests_per_second,
            previous_total_requests_per_second=previous_result[0].total_requests_per_second
        )

    return GetLoadTestResultDetailsResponse(details=details)


async def crate_load_test_result(
        request: CreateLoadTestResultRequest,
        session: AsyncSession
) -> GetLoadTestResultDetailsResponse:
    result = await LoadTestResultsModel.create(session, **request.model_dump())

    return GetLoadTestResultDetailsResponse(
        details=LoadTestResultDetails.model_validate(result),
    )
