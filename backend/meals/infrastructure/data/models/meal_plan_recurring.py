import uuid
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from app.data.base import Base

class MealPlanRecurringModel(Base):
    __tablename__ = "meal_plan_recurring"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    meal_id = Column(String(36), ForeignKey("meals.id", ondelete="CASCADE"), nullable=True)
    target_date = Column(Date, nullable=False)
    order_index = Column(Integer, nullable=False, default=0)