import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from apps.results.schema.methods import GetMethodsQuery, Method, GetMethodsResponse, GetMethodDetailsQuery, \
    GetMethodDetailsResponse, MethodDetails
from services.postgres.models import MethodResultsModel


async def get_methods(query: GetMethodsQuery, session: AsyncSession) -> GetMethodsResponse:
    results = await MethodResultsModel.filter(
        session,
        distinct=(MethodResultsModel.method,),
        clause_filter=(MethodResultsModel.service == query.service,)
    )

    methods: list[Method] = []
    for result in results:
        (response_time, number_of_requests, requests_per_second) = await asyncio.gather(
            result.get_average_response_time(session),
            result.get_average_number_of_requests(session),
            result.get_average_requests_per_second(session),
        )

        methods.append(
            Method(
                method=result.method,
                service=result.service,
                average_response_time=response_time,
                average_number_of_requests=number_of_requests,
                average_requests_per_second=requests_per_second,
            )
        )

    return GetMethodsResponse(methods=methods)


async def get_method_details(
        query: GetMethodDetailsQuery,
        session: AsyncSession
) -> GetMethodDetailsResponse:
    result = await MethodResultsModel.get(
        session,
        clause_filter=(MethodResultsModel.method == query.method,)
    )

    (
        response_time,
        min_response_time,
        max_response_time,
        number_of_requests,
        number_of_failures,
        requests_per_second,
        failures_per_second
    ) = await asyncio.gather(
        result.get_average_response_time(session),
        result.get_average_min_response_time(session),
        result.get_average_max_response_time(session),
        result.get_average_number_of_requests(session),
        result.get_average_number_of_failures(session),
        result.get_average_requests_per_second(session),
        result.get_average_failures_per_second(session),
    )

    return GetMethodDetailsResponse(
        details=MethodDetails(
            method=result.method,
            service=result.service,
            average_response_time=response_time,
            average_number_of_requests=number_of_requests,
            average_requests_per_second=requests_per_second,
            average_max_response_time=max_response_time,
            average_min_response_time=min_response_time,
            average_number_of_failures=number_of_failures,
            average_failures_per_second=failures_per_second
        )
    )
