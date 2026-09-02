import uuid
from sqlalchemy import Column, String, Date, Boolean, DateTime, ForeignKey, UniqueConstraint, Index, func
from app.data.base import Base

class VoucherModel(Base):
    __tablename__ = "voucher"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    meal_plan_id = Column(String(36), ForeignKey("meal_plan.id", ondelete="CASCADE"), nullable=False)
    reservation_date = Column(Date, nullable=False)
    is_used = Column(Boolean, nullable=False, default=False)
    redeemed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "reservation_date", name="uq_voucher_user_date"),
        Index("idx_voucher_user", "user_id"),
        Index("idx_voucher_mealplan", "meal_plan_id"),
    )