from datetime import date, datetime
from typing import Iterable
import uuid
from pydantic import BaseModel

from .base_response import BaseResponseModel


class CreateRecordRequestModel(BaseModel):
    name: str
    birth: date
    phone: str
    patient_nik: str

class RecordCreatedModel(BaseModel):
    patient_id: uuid.UUID
    record_id: uuid.UUID

class RecordCreatedResponseModel(BaseResponseModel):
    data: RecordCreatedModel

class PatientModel(BaseModel):
    nik: str
    birth: date
    classification: str | None = None
    id: uuid.UUID
    name: str
    phone: str
    recommendation: str | None = None

class PatientResponseModel(BaseResponseModel):
    data: Iterable[PatientModel]

class ControlModel(BaseModel):
    patient_id: uuid.UUID
    nik: str
    name: str
    last_control: datetime

class ControlResponseModel(BaseResponseModel):
    data: Iterable[ControlModel]