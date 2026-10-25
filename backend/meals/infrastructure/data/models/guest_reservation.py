import uuid
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    false,
    func,
)
from app.data.base import Base


class GuestReservationModel(Base):
    __tablename__ = "guest_reservation"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    meal_plan_id = Column(String(36), ForeignKey("meal_plan.id", ondelete="CASCADE"), nullable=False)
    unit_id = Column(String(36), ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    invited_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    guest_count = Column(Integer, nullable=False)
    is_used = Column(Boolean, nullable=False, default=False, server_default=false())
    reservation_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("meal_plan_id", "unit_id", "invited_by", name="uq_guest_plan_unit_inviter"),
        CheckConstraint("guest_count >= 1", name="ck_guest_count_positive"),
        Index("idx_guest_plan", "meal_plan_id"),
        Index("idx_guest_date_unit", "reservation_date", "unit_id"),
    )