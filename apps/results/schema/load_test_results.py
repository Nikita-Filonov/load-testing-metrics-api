from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import BaseModel, Field, field_validator, computed_field, ConfigDict

from utils.schema.database_model import DatabaseModel
from utils.schema.paginration_model import PaginationResponse
from utils.schema.query_model import PaginationQuery


class LoadTestResultCompare(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    previous_id: int | None = Field(default=None, alias="previousId")
    current_total_requests_per_second: float = Field(alias="currentTotalRequestsPerSecond")
    previous_total_requests_per_second: float = Field(
        default=0.0,
        alias="previousTotalRequestsPerSecond"
    )

    @classmethod
    def get_compare(cls, current: float, previous: float) -> float:
        if current == 0.0 or previous == 0.0:
            return 0.0

        return round(((current - previous) / previous) * 100, 2)

    @computed_field(alias="totalRequestsPerSecondCompare")
    def total_requests_per_second_compare(self) -> float:
        return self.get_compare(
            previous=self.previous_total_requests_per_second,
            current=self.current_total_requests_per_second
        )


class LoadTestResult(DatabaseModel):
    id: int
    service: str
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    total_requests: int = Field(alias="totalRequests")
    number_of_users: int = Field(alias="numberOfUsers")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_title: str | None = Field(alias="triggerCIProjectTitle")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")

    compare: LoadTestResultCompare | None = None

    @field_validator('total_requests_per_second')
    def validate_total_requests_per_second(cls, total_requests_per_second: float) -> float:
        return round(total_requests_per_second, 2)


class LoadTestResultDetails(LoadTestResult):
    total_failures: int = Field(alias="totalFailures")
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")

    @field_validator('max_response_time')
    def validate_max_response_time(cls, max_response_time: float) -> float:
        return round(max_response_time, 2)

    @field_validator('min_response_time')
    def validate_min_response_time(cls, min_response_time: float) -> float:
        return round(min_response_time, 2)

    @field_validator('total_failures_per_second')
    def validate_total_failures_per_second(cls, total_failures_per_second: float) -> float:
        return round(total_failures_per_second, 2)


class GetLoadTestResultsQuery(PaginationQuery):
    service: str

    @classmethod
    async def as_query(
            cls,
            limit: int = Query(default=50),
            offset: int = Query(default=0),
            service: str = Query()
    ) -> Self:
        return GetLoadTestResultsQuery(
            limit=limit,
            offset=offset,
            service=service
        )


class GetLoadTestResultsResponse(PaginationResponse[LoadTestResult]):
    ...


class GetLoadTestResultDetailsResponse(BaseModel):
    details: LoadTestResultDetails


class CreateLoadTestResultRequest(BaseModel):
    service: str
    started_at: datetime = Field(alias="startedAt")
    finished_at: datetime = Field(alias="finishedAt")
    total_requests: int = Field(alias="totalRequests")
    number_of_users: int = Field(alias="numberOfUsers")
    trigger_ci_pipeline_url: str | None = Field(alias="triggerCIPipelineUrl")
    trigger_ci_project_title: str | None = Field(alias="triggerCIProjectTitle")
    trigger_ci_project_version: str | None = Field(alias="triggerCIProjectVersion")
    load_tests_ci_pipeline_url: str | None = Field(alias="loadTestsCIPipelineUrl")
    total_requests_per_second: float = Field(alias="totalRequestsPerSecond")
    total_failures: int = Field(alias="totalFailures")
    total_failures_per_second: float = Field(alias="totalFailuresPerSecond")
    average_response_time: float = Field(alias="averageResponseTime")
    max_response_time: float = Field(alias="maxResponseTime")
    min_response_time: float = Field(alias="minResponseTime")
