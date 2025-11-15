from fastapi import APIRouter, Depends
from app.utils import get_orgs_service
from app.domains.organizations.service import OrganizationsService
from app.domains.organizations.schemas.buildings import (
    BuildingCreate,
    BuildingOut
)
from app.endpoints.v1.api_key_auth import api_key_header


router = APIRouter(prefix="/v1", tags=["Здания"])

@router.post(
    "/buildings",
    dependencies=[Depends(api_key_header)],
    response_model=BuildingOut,
    summary="Создать здание",
)
async def create_building(
    payload: BuildingCreate,
    service: OrganizationsService = Depends(get_orgs_service),
) -> BuildingOut:
    """
    Создаёт новое здание.

    Поля:
    - `address` — адрес здания  
    - `latitude` — широта  
    - `longitude` — долгота  

    Возвращает созданное здание.
    """
    return await service.repo.create_building(
        payload.address,
        payload.latitude,
        payload.longitude,
    )


@router.get(
    "/buildings",
    dependencies=[Depends(api_key_header)],
    response_model=list[BuildingOut],
    summary="Получить список всех зданий",
)
async def list_buildings(
    service: OrganizationsService = Depends(get_orgs_service),
) -> list[BuildingOut]:
    """
    Возвращает список всех зданий со всеми их характеристиками.
    """
    return await service.repo.list_buildings()