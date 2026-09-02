import uuid
from sqlalchemy import Column, String, Date, ForeignKey, UniqueConstraint, Index
from app.data.base import Base

class MealPlanModel(Base):
    __tablename__ = "meal_plan"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_date = Column(Date, nullable=False)
    meal_id = Column(String(36), ForeignKey("meals.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("plan_date", "meal_id", name="uq_mealplan_date_meal"),
        Index("idx_mealplan_date", "plan_date"),
    )