import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Index, CheckConstraint, func
from app.data.base import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone = Column(String(11), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    personnel_code = Column(String(4), nullable=True, unique=True)
    rfid_card_id = Column(String(10), nullable=True, unique=True)
    unit_id = Column(String(36), ForeignKey("units.id", ondelete="SET NULL"), nullable=True)
    is_blocked = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_user_phone", "phone"),
        Index("idx_user_unit", "unit_id"),
        CheckConstraint("phone ~ '^09[0-9]{9}$'", name="ck_user_phone_format"),
        CheckConstraint("personnel_code ~ '^[0-9]{4}$'", name="ck_user_personnel_code_format"),
        CheckConstraint("rfid_card_id ~ '^[0-9A-Fa-f]{10}$'", name="ck_user_rfid_format"),
    )