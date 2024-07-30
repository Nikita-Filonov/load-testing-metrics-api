from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import Field

from utils.schema.query_model import QueryModel


class GetResultsAnalyticsQuery(QueryModel):
    service: str
    start_datetime: datetime = Field(alias="startDatetime")
    end_datetime: datetime = Field(alias="endDatetime")

    @classmethod
    async def as_query(
            cls,
            service: str,
            start_datetime: datetime = Query(alias="startDatetime"),
            end_datetime: datetime = Query(alias="endDatetime")
    ) -> Self:
        return GetResultsAnalyticsQuery(
            service=service,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
