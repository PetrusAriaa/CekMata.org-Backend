from sqlalchemy import Column, String, Boolean, DateTime, text
from sqlalchemy.sql import func

from db import Base

class Users(Base):
    __tablename__ = "user"

    id = Column(String(255), primary_key=True, index=True)
    username = Column(String(255), nullable=True)
    password = Column(String(255),  nullable=True)
    deleted_at = Column(DateTime, server_default=func.now(), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))
    last_login = Column(DateTime, nullable=True)