from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped

from utils.clients.postgres.mixin_model import MixinModel


class ServicesModel(MixinModel):
    __tablename__ = "services"

    name: Mapped[str] = Column(String(100), nullable=False, primary_key=True)
    url: Mapped[str] = Column(String(250), nullable=False)
