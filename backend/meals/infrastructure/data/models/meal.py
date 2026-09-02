import uuid
from sqlalchemy import Column, String, Boolean, Text
from app.data.base import Base

class MealModel(Base):
    __tablename__ = "meals"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    photo_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)