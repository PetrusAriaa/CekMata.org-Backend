from sqlalchemy import UUID, Column, String, DateTime, text
from sqlalchemy.sql import func

from db import Base

class Patients(Base):
    __tablename__ = "patient"

    id = Column(UUID, primary_key=True, unique=True, server_default=text("gen_random_uuid()"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))
    deleted_at = Column(DateTime, server_default=text("NULL ON DELETE CURRENT_TIMESTAMP"))
    fk_patient_id = Column(UUID)
    fk_patient_code = Column(String(9))
    patient_name = Column(String(255))
    last_control = Column(DateTime, server_default=func.now())