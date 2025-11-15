from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id", ondelete="SET NULL"), nullable=True)

    children = relationship("Activity", backref="parent", remote_side=[id])

    organizations = relationship(
        "Organization",
        secondary="organization_activities",
        back_populates="activities",
    )
