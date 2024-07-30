from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class LoadTestResultsModel(MixinModel):
    __tablename__ = "load_test_results"

    id: Mapped[int] = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    trigger_ci_pipeline_url: Mapped[str | None] = Column(String, nullable=True)
    trigger_ci_project_title: Mapped[str | None] = Column(String, nullable=True)
    trigger_ci_project_version: Mapped[str | None] = Column(String, nullable=True)
    load_tests_ci_pipeline_url: Mapped[str | None] = Column(String, nullable=True)
    number_of_users: Mapped[int] = Column(Integer, nullable=False)
    total_requests: Mapped[int] = Column(Integer, nullable=False)
    total_failures: Mapped[int] = Column(Integer, nullable=False)
    max_response_time: Mapped[float] = Column(Float, nullable=False)
    min_response_time: Mapped[float] = Column(Float, nullable=False)
    average_response_time: Mapped[float] = Column(Float, nullable=False)
    total_requests_per_second: Mapped[float] = Column(Float, nullable=False)
    total_failures_per_second: Mapped[float] = Column(Float, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    started_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)

    service: Mapped[str] = Column(
        String,
        ForeignKey("services.name", ondelete="CASCADE"),
        nullable=False
    )
