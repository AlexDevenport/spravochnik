from pydantic import BaseModel
from typing import List, Optional
from .activities import ActivityOut
from .buildings import BuildingOut


class OrgCreateSchema(BaseModel):
    name: str
    phones: List[str]
    building_id: int
    activity_ids: List[int]


class OrgOutSchema(BaseModel):
    id: int
    name: str
    phones: List[str]
    building: Optional[BuildingOut]
    activities: List[ActivityOut]

    class Config:
        from_attributes = True

    @classmethod
    def from_model(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            phones=[p.number for p in obj.phones],
            building=BuildingOut.from_orm(obj.building) if obj.building else None,
            activities=[ActivityOut.from_orm(a) for a in obj.activities],
        )
