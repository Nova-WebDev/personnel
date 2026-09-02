import uuid
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from app.data.base import Base

class UnitModel(Base):
    __tablename__ = "units"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("name", "branch_id", name="uq_unit_name_branch"),
    )