from sqlalchemy.ext.asyncio import AsyncSession

from apps.services.schema.services import GetServicesResponse, Service
from services.postgres.models import ServicesModel


async def get_services(session: AsyncSession) -> GetServicesResponse:
    services = await  ServicesModel.filter(session)

    return GetServicesResponse(
        services=[Service.model_validate(service) for service in services]
    )
