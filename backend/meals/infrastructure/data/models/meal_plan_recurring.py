import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from app.data.base import Base

class MealPlanRecurringModel(Base):
    __tablename__ = "meal_plan_recurring"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    target_date = Column(Date, nullable=False, unique=True)
    meal_id = Column(String(36), ForeignKey("meals.id", ondelete="SET NULL"), nullable=True)