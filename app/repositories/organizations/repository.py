from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models.organization import Organization
from .models.building import Building
from .models.activity import Activity
from .models.phone import OrganizationPhone
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

class OrganizationsRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    # BUILDINGS
    async def create_building(self, address: str, lat: float, lon: float) -> Building:
        building = Building(address=address, latitude=lat, longitude=lon)
        self.session.add(building)
        await self.session.commit()
        await self.session.refresh(building)
        return building

    async def list_buildings(self) -> list[Building]:
        q = select(Building)
        result = await self.session.execute(q)
        return result.scalars().all()

    # ACTIVITIES
    async def create_activity(self, name: str, parent_id: int | None) -> Activity:
        activity = Activity(name=name, parent_id=parent_id)
        self.session.add(activity)
        await self.session.commit()
        await self.session.refresh(activity)
        return activity

    async def list_activities(self) -> list[Activity]:
        result = await self.session.execute(select(Activity))
        return result.scalars().all()

    # ORGANIZATIONS
    async def get_org(self, org_id: int) -> Organization | None:
        stmt = (
            select(Organization)
            .where(Organization.id == org_id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_org(self, org: Organization) -> Organization:
        self.session.add(org)
        await self.session.commit()
        await self.session.refresh(org)

        stmt = (
            select(Organization)
            .where(Organization.id == org.id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


    async def list_by_building(self, building_id: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .where(Organization.building_id == building_id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_by_activities(self, activity_ids: list[int]) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
            .distinct()
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def search_by_name(self, q: str) -> list[Organization]:
        stmt = (
            select(Organization)
            .where(Organization.name.ilike(f"%{q}%"))
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # GEO
    async def list_in_bbox(self, min_lat, min_lon, max_lat, max_lon):
        stmt = (
            select(Organization)
            .join(Organization.building)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon)
            )
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_in_radius(self, lat: float, lon: float, radius_km: float):
        # 1 градус ≈ 111 км
        degree_km = radius_km / 111

        stmt = (
            select(Organization)
            .join(Organization.building)
            .where(
                func.pow(Building.latitude - lat, 2)
                + func.pow(Building.longitude - lon, 2)
                <= func.pow(degree_km, 2)
            )
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities),
                selectinload(Organization.phones),
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()