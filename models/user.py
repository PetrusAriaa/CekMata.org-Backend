from sqlalchemy import UUID, Column, Date, String, DateTime, text
from sqlalchemy.sql import func

from db import Base

class Users(Base):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))
    deleted_at = Column(DateTime, server_default=text("NULL ON DELETE CURRENT_TIMESTAMP"))
    username = Column(String(32))
    password = Column(String(255))
    last_login = Column(DateTime, nullable=True)