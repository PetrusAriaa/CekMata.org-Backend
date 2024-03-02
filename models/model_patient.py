from sqlalchemy import UUID, Column, Date, ForeignKey, String, DateTime, text
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from db import Base

class Patients(Base):
    __tablename__ = "patients"

    id = Column(UUID, primary_key=True, unique=True, server_default=text("gen_random_uuid()"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    code = Column(String(9))
    name = Column(String(255))
    birth = Column(Date)
    phone = Column(String(20))
    classification = Column(String(255), nullable=True)
    recommendation = Column(String(255), nullable=True)