import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String, Boolean, DateTime, Enum as SAEnum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from personnel.core.entities.position import PersonnelPosition


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    units: Mapped[list["Unit"]] = relationship(back_populates="branch")


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))

    branch: Mapped["Branch"] = relationship(back_populates="units")


class Personnel(Base):
    __tablename__ = "personnel"

    uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    personnel_id: Mapped[str] = mapped_column(String(20), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    photo_path: Mapped[str] = mapped_column(String(255))
    position: Mapped[PersonnelPosition] = mapped_column(SAEnum(PersonnelPosition))
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id"), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    branch: Mapped["Branch"] = relationship()
    unit: Mapped["Unit | None"] = relationship()