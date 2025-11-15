from pydantic import BaseModel
from typing import Optional


class ActivityCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class ActivityOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]

    class Config:
        from_attributes = True
