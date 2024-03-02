from sqlalchemy import UUID, Column, ForeignKey, String, DateTime, text
from sqlalchemy.sql import func

from db import Base

class Controls(Base):
    __tablename__ = "controls"

    id = Column(UUID, primary_key=True, unique=True, server_default=text("gen_random_uuid()"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    fk_patient_id = Column(UUID, ForeignKey('patients.id'))
    fk_patient_code = Column(String(9), ForeignKey('patients.code'))
    patient_name = Column(String(255))
    last_control = Column(DateTime, server_default=func.now())