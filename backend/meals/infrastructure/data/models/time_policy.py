import uuid
from sqlalchemy import Column, String, Integer, Time
from app.data.base import Base

class MealPlanTimePolicyModel(Base):
    __tablename__ = "meal_plan_time_policy"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    day_index = Column(Integer, unique=True, nullable=False)
    offset_days = Column(Integer, nullable=False)
    cutoff_time = Column(Time, nullable=False)