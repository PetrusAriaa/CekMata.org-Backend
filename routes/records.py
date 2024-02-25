from datetime import date
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .auth import validate_token


class PatientRecords(BaseModel):
    patient_id: str
    patient_name: str
    start_consultation_date: date
    last_consultation_date: date
    issue: str

DUMMY_DATA = {
    "patient_id": "idkbro123123",
    "patient_name": "Him Da Gowd",
    "start_consultation_date": date(2024, 1, 10),
    "last_consultation_date": date(2024, 1, 12),
    "issue": "skill issue"
}

records_router = APIRouter(tags=["Records"], dependencies=[Depends(validate_token)])


@records_router.get("/")
def get_patient_records():
    return DUMMY_DATA