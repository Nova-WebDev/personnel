import uuid
from sqlalchemy import Column, String, Integer, Enum as SAEnum
from app.data.base import Base
from meals.core.entities.week_day import WeekDay


class MealPlanTimePolicyModel(Base):
    __tablename__ = "meal_plan_time_policy"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    target_weekday = Column(SAEnum(WeekDay), unique=True, nullable=False)
    cutoff_hours_before = Column(Integer, nullable=False)