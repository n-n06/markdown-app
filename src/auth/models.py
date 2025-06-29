from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from src.db import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    id : Mapped[int] = MappedColumn(primary_key=True)
    notes = relationship("Note", back_populates="user")
