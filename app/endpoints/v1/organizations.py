from fastapi import APIRouter, Depends
from app.endpoints.v1.exceptions import OrganizationNotFoundException
from app.utils import get_orgs_service
from app.domains.organizations.service import OrganizationsService, NotFound
from app.domains.organizations.schemas.organizations import (
    OrgCreateSchema,
    OrgOutSchema
)
from app.endpoints.v1.api_key_auth import api_key_header


router = APIRouter(prefix="/v1", tags=["Организации"])


@router.post(
    "/organizations",
    dependencies=[Depends(api_key_header)],
    response_model=OrgOutSchema,
    summary="Создать организацию",
)
async def create_org(
    payload: OrgCreateSchema,
    service: OrganizationsService = Depends(get_orgs_service),
) -> OrgOutSchema:
    """
    Создаёт организацию.

    Поля:
    - `name` — название  
    - `phones` — список телефонов  
    - `building_id` — ID здания  
    - `activity_ids` — список видов деятельности  
    """
    return await service.create_organization(payload)


@router.get(
    "/organizations/in-bbox",
    dependencies=[Depends(api_key_header)],
    response_model=list[OrgOutSchema],
    summary="Организации внутри прямоугольной области",
)
async def orgs_in_bbox(
    min_lat: float,
    min_lon: float,
    max_lat: float,
    max_lon: float,
    service: OrganizationsService = Depends(get_orgs_service),
) -> list[OrgOutSchema]:
    """
    Возвращает организации в прямоугольной области карты.
    """
    return await service.list_in_bbox(min_lat, min_lon, max_lat, max_lon)


@router.get(
    "/organizations/in-radius",
    dependencies=[Depends(api_key_header)],
    response_model=list[OrgOutSchema],
    summary="Организации в радиусе точки",
)
async def orgs_in_radius(
    lat: float,
    lon: float,
    radius_km: float = 1.0,
    service: OrganizationsService = Depends(get_orgs_service),
) -> list[OrgOutSchema]:
    """
    Возвращает организации в пределах указанного радиуса (в километрах)
    от точки (`lat`, `lon`).
    """
    return await service.list_in_radius(lat, lon, radius_km)


@router.get(
    "/organizations/search",
    dependencies=[Depends(api_key_header)],
    response_model=list[OrgOutSchema],
    summary="Поиск организации по названию",
)
async def search_orgs(
    q: str,
    service: OrganizationsService = Depends(get_orgs_service),
) -> list[OrgOutSchema]:
    """
    Поиск организаций по частичному совпадению названия.

    Пример:
    - `?q=рога` → "Рога и Копыта".
    """
    return await service.search_by_name(q)


@router.get(
    "/organizations/by-building/{building_id}",
    dependencies=[Depends(api_key_header)],
    response_model=list[OrgOutSchema],
    summary="Организации в указанном здании",
)
async def orgs_by_building(
    building_id: int,
    service: OrganizationsService = Depends(get_orgs_service),
) -> list[OrgOutSchema]:
    """
    Возвращает список организаций,
    которые расположены в указанном **здании**.
    """
    return await service.list_by_building(building_id)


@router.get(
    "/organizations/by-activity/{activity_id}",
    dependencies=[Depends(api_key_header)],
    response_model=list[OrgOutSchema],
    summary="Организации по виду деятельности",
)
async def orgs_by_activity(
    activity_id: int,
    depth: int = 3,
    service: OrganizationsService = Depends(get_orgs_service),
) -> list[OrgOutSchema]:
    """
    Возвращает список организаций по виду деятельности,
    включая вложенные категории до 3 уровней.
    """
    return await service.list_by_activity(activity_id, max_depth=depth)


@router.get(
    "/organizations/{org_id}",
    dependencies=[Depends(api_key_header)],
    response_model=OrgOutSchema,
    summary="Получить организацию по ID",
)
async def get_org(
    org_id: int,
    service: OrganizationsService = Depends(get_orgs_service),
) -> OrgOutSchema:
    """
    Возвращает информацию об организации по её идентификатору.
    """
    try:
        return await service.get(org_id)
    except NotFound:
        raise OrganizationNotFoundException