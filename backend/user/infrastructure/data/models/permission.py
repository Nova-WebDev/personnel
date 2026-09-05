import uuid
from sqlalchemy import Column, String, Enum as SAEnum, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.data.base import Base
from user.core.entities.permission_level import PermissionLevel

class PermissionModel(Base):
    __tablename__ = "permissions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    level = Column(SAEnum(PermissionLevel), nullable=False)
    group_id = Column(String(36), ForeignKey("units.id", ondelete="CASCADE"), nullable=True)

    user = relationship("UserModel", back_populates="permissions")

    __table_args__ = (
        Index("idx_permission_user", "user_id"),
        Index("idx_permission_group_level", "group_id", "level"),
        UniqueConstraint("user_id", "level", "group_id", name="uq_permission_user_level_group"),
    )