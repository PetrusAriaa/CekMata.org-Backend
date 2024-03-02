from sqlalchemy import UUID, Column, Date, String, DateTime, text
from sqlalchemy.sql import func

from db import Base

class Patients(Base):
    __tablename__ = "patient"

    id = Column(UUID, primary_key=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))
    deleted_at = Column(DateTime, server_default=text("NULL ON DELETE CURRENT_TIMESTAMP"))
    code = Column(String(9))
    name = Column(String(255))
    birth = Column(Date)
    phone = Column(String(20))
    classification = Column(String(255), nullable=True)
    recommendation = Column(String(255), nullable=True)