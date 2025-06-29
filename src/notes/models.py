from sqlalchemy import DateTime, func, String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base
from datetime import datetime

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_edited: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)   
    user = relationship("User", back_populates="notes")
