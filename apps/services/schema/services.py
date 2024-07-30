from pydantic import BaseModel, HttpUrl

from utils.schema.database_model import DatabaseModel


class Service(DatabaseModel):
    url: HttpUrl
    name: str


class GetServicesResponse(BaseModel):
    services: list[Service]
