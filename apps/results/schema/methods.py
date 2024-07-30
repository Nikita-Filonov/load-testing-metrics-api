from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, field_validator

from utils.schema.database_model import DatabaseModel
from utils.schema.query_model import QueryModel


class Method(DatabaseModel):
    method: str
    service: str
    average_response_time: float = Field(alias="averageResponseTime")
    average_number_of_requests: float = Field(alias="averageNumberOfRequests")
    average_requests_per_second: float = Field(alias="averageRequestsPerSecond")

    @field_validator('average_response_time')
    def validate_average_response_time(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('average_requests_per_second')
    def validate_average_requests_per_second(cls, value: float) -> float:
        return round(value, 2)


class MethodDetails(Method):
    average_max_response_time: float = Field(alias="averageMaxResponseTime")
    average_min_response_time: float = Field(alias="averageMinResponseTime")
    average_number_of_failures: float = Field(alias="averageNumberOfFailures")
    average_failures_per_second: float = Field(alias="averageFailuresPerSecond")

    @field_validator('average_max_response_time')
    def validate_average_max_response_time(cls, value: float) -> float:
        return round(value, 2)

    @field_validator('average_min_response_time')
    def validate_average_min_response_time(cls, value: float) -> float:
        return round(value, 2)


class GetMethodsQuery(QueryModel):
    service: str

    @classmethod
    async def as_query(cls, service: str = Query()) -> Self:
        return GetMethodsQuery(service=service)


class GetMethodsResponse(BaseModel):
    methods: list[Method]


class GetMethodDetailsQuery(QueryModel):
    method: str

    @classmethod
    async def as_query(cls, method: str = Query()) -> Self:
        return GetMethodDetailsQuery(method=method)


class GetMethodDetailsResponse(BaseModel):
    details: MethodDetails
