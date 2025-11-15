from fastapi import APIRouter, Depends
from app.utils import get_orgs_service
from app.domains.organizations.service import OrganizationsService
from app.domains.organizations.schemas.activities import (
    ActivityCreate,
    ActivityOut
)
from app.endpoints.v1.api_key_auth import api_key_header


router = APIRouter(prefix="/v1", tags=["Виды деятельности"])

@router.post(
    "/activities",
    dependencies=[Depends(api_key_header)],
    response_model=ActivityOut,
    summary="Создать вид деятельности",
)
async def create_activity(
    payload: ActivityCreate,
    service: OrganizationsService = Depends(get_orgs_service),
) -> ActivityOut:
    """
    Создаёт новый вид деятельности.

    Поля:
    - `name` — название  
    - `parent_id` — родительская категория (для дерева до 3 уровней)
    """
    return await service.repo.create_activity(payload.name, payload.parent_id)


@router.get(
    "/activities",
    dependencies=[Depends(api_key_header)],
    response_model=list[ActivityOut],
    summary="Получить список всех видов деятельности",
)
async def list_activities(
    service: OrganizationsService = Depends(get_orgs_service),
) -> list[ActivityOut]:
    """
    Возвращает список всех видов деятельности.
    """
    return await service.repo.list_activities()