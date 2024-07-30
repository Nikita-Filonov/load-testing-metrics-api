from datetime import datetime

from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class MethodResultsModel(MixinModel):
    __tablename__ = "method_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    method: Mapped[str] = Column(String(200), nullable=False)
    protocol: Mapped[str] = Column(String(20), nullable=False)
    number_of_requests: Mapped[int] = Column(Integer, nullable=False)
    number_of_failures: Mapped[int] = Column(Integer, nullable=False)
    max_response_time: Mapped[float] = Column(Float, nullable=False)
    min_response_time: Mapped[float] = Column(Float, nullable=False)
    total_response_time: Mapped[float] = Column(Float, nullable=False)
    requests_per_second: Mapped[float] = Column(Float, nullable=False)
    failures_per_second: Mapped[float] = Column(Float, nullable=False)
    average_response_time: Mapped[float] = Column(Float, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    service: Mapped[str] = Column(
        String,
        ForeignKey("services.name", ondelete="CASCADE"),
        nullable=False
    )
    load_test_results_id: Mapped[int] = Column(
        Integer,
        ForeignKey("load_test_results.id", ondelete="CASCADE"),
        nullable=False
    )

    async def get_average_response_time(self, session: AsyncSession) -> float:
        return await self.average(
            session,
            column=MethodResultsModel.average_response_time,
            clause_filter=(MethodResultsModel.method == self.method,)
        )

    async def get_average_number_of_requests(self, session: AsyncSession) -> float:
        return await self.average(
            session,
            column=MethodResultsModel.number_of_requests,
            clause_filter=(MethodResultsModel.method == self.method,)
        )

    async def get_average_requests_per_second(self, session: AsyncSession) -> float:
        return await self.average(
            session,
            column=MethodResultsModel.requests_per_second,
            clause_filter=(MethodResultsModel.method == self.method,)
        )

    async def get_average_min_response_time(self, session: AsyncSession) -> float:
        return await self.average(
            session,
            column=MethodResultsModel.min_response_time,
            clause_filter=(MethodResultsModel.method == self.method,)
        )

    async def get_average_max_response_time(self, session: AsyncSession) -> float:
        return await self.average(
            session,
            column=MethodResultsModel.max_response_time,
            clause_filter=(MethodResultsModel.method == self.method,)
        )

    async def get_average_number_of_failures(self, session: AsyncSession) -> float:
        return await self.average(
            session,
            column=MethodResultsModel.number_of_failures,
            clause_filter=(MethodResultsModel.method == self.method,)
        )

    async def get_average_failures_per_second(self, session: AsyncSession) -> float:
        return await self.average(
            session,
            column=MethodResultsModel.failures_per_second,
            clause_filter=(MethodResultsModel.method == self.method,)
        )
