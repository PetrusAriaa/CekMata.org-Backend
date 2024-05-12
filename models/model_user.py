from sqlalchemy import UUID, Column, Date, String, DateTime, text
from sqlalchemy.sql import func

from db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, unique=True, server_default=text("gen_random_uuid()"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    username = Column(String(32))
    password = Column(String(255))
    last_login = Column(DateTime, nullable=True)