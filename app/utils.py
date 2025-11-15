from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database import async_session_maker
from app.repositories.organizations.repository import OrganizationsRepository
from app.domains.organizations.service import OrganizationsService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_orgs_repo(
    session: AsyncSession = Depends(get_session),
) -> OrganizationsRepository:
    """Фабрика репозитория организаций."""
    return OrganizationsRepository(session)


def get_orgs_service(
    repo: OrganizationsRepository = Depends(get_orgs_repo),
) -> OrganizationsService:
    """Фабрика сервиса организаций."""
    return OrganizationsService(repo=repo)
