from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from app.repositories.organizations.repository import OrganizationsRepository
from app.repositories.organizations.models.phone import OrganizationPhone
from app.repositories.organizations.models.activity import Activity
from .schemas.organizations import OrgCreateSchema, OrgOutSchema


class NotFound(Exception):
    pass


class OrganizationsService:
    def __init__(self, repo: OrganizationsRepository):
        self.repo = repo

    async def get(self, org_id: int) -> OrgOutSchema:
        org = await self.repo.get_org(org_id)
        if not org:
            raise NotFound
        return OrgOutSchema.from_model(org)

    async def create_organization(self, data: OrgCreateSchema) -> OrgOutSchema:
        # создаём ORM-объект Organization (импортируй модель)
        from app.repositories.organizations.models.organization import Organization
        org = Organization(name=data.name, building_id=data.building_id)

        org.phones = [OrganizationPhone(number=p) for p in data.phones]

        # связываем activities по id
        org.activities = [
            await self.repo.session.get(Activity, a_id)
            for a_id in data.activity_ids
        ]
        org = await self.repo.create_org(org)
        return OrgOutSchema.from_model(org)

    # FILTERS
    async def list_by_building(self, building_id: int):
        orgs = await self.repo.list_by_building(building_id)
        return [OrgOutSchema.from_model(o) for o in orgs]

    async def list_by_activity(self, activity_id: int, max_depth=3):
        ids = await self._expand_activity_tree(activity_id, max_depth)
        orgs = await self.repo.list_by_activities(ids)
        return [OrgOutSchema.from_model(o) for o in orgs]

    async def search_by_name(self, q: str):
        orgs = await self.repo.search_by_name(q)
        return [OrgOutSchema.from_model(o) for o in orgs]

    async def list_in_bbox(self, min_lat, min_lon, max_lat, max_lon):
        orgs = await self.repo.list_in_bbox(min_lat, min_lon, max_lat, max_lon)
        return [OrgOutSchema.from_model(o) for o in orgs]

    async def list_in_radius(self, lat, lon, radius_km):
        orgs = await self.repo.list_in_radius(lat, lon, radius_km)
        return [OrgOutSchema.from_model(o) for o in orgs]

    # ---------- ACTIVITY TREE EXPANSION ----------
    async def _expand_activity_tree(self, root_id: int, depth: int) -> list[int]:
        to_visit = [root_id]
        visited = set()

        for _ in range(depth):
            # SELECT id FROM activity WHERE parent_id IN (...)
            result = await self.repo.session.execute(
                select(Activity.id).where(Activity.parent_id.in_(to_visit))
            )
            children = result.scalars().all()

            visited.update(to_visit)
            to_visit = children

            if not children:
                break

        visited.update(to_visit)
        return list(visited)
