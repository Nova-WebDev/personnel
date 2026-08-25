import uuid as uuid_lib
from datetime import datetime

from sqlalchemy import ForeignKey, String, Boolean, DateTime, Enum as SAEnum, Index, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.base import Base
from personnel.core.entities.position import PersonnelPosition


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    units: Mapped[list["Unit"]] = relationship(
        back_populates="branch",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Unit(Base):
    __tablename__ = "units"
    __table_args__ = (
        UniqueConstraint("name", "branch_id", name="uq_unit_name_branch_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id", ondelete="CASCADE"), index=True)

    branch: Mapped["Branch"] = relationship(back_populates="units")


class Personnel(Base):
    __tablename__ = "personnel"
    __table_args__ = (
        Index(
            "ix_personnel_first_name_trgm",
            "first_name",
            postgresql_using="gin",
            postgresql_ops={"first_name": "gin_trgm_ops"},
        ),
        Index(
            "ix_personnel_last_name_trgm",
            "last_name",
            postgresql_using="gin",
            postgresql_ops={"last_name": "gin_trgm_ops"},
        ),
    )

    uuid: Mapped[uuid_lib.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid_lib.uuid4)
    personnel_id: Mapped[str] = mapped_column(String(20), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    photo_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    position: Mapped[PersonnelPosition | None] = mapped_column(
        SAEnum(PersonnelPosition),
        nullable=True,
    )
    branch_id: Mapped[int | None] = mapped_column(ForeignKey("branches.id", ondelete="SET NULL"), nullable=True, index=True)
    unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id", ondelete="SET NULL"), nullable=True, index=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    branch: Mapped["Branch | None"] = relationship()
    unit: Mapped["Unit | None"] = relationship()