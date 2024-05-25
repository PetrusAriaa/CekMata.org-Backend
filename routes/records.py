from datetime import date, datetime, time
import uuid

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from .auth import validate_token
from db import get_db
from dto import CreateRecordRequestModel, RecordCreatedResponseModel, \
    PatientResponseModel, PatientModel, ControlModel, ControlResponseModel, \
    ActivePatientModel, ActivePatientResponseModel, PatientClassificationRequestModel
from models import Patients, Controls
from utils.validate_uuid import validate_uuid


records_router = APIRouter(tags=["Records"], dependencies=[Depends(validate_token)])


def __create_patient(patient_data: CreateRecordRequestModel, db: Session):
    patient_id = uuid.uuid4()
    current_date = datetime.now()
    last_control = current_date
    record_id = uuid.uuid4()
    
    patient = db.query(Patients) \
                .filter(Patients.nik == patient_data.patient_nik).first()
    if patient is not None:
        patient_id = patient.id
        record = db.query(Controls) \
            .filter(Controls.fk_patient_id == patient_id) \
            .order_by(Controls.created_at.desc()).first()
        last_control = record.created_at
    
    else:
        patient = Patients(
            id = patient_id,
            nik = patient_data.patient_nik,
            name = patient_data.name,
            birth = patient_data.birth,
            phone = patient_data.phone,
            created_at = current_date
        )
        db.add(patient)
        db.commit()
    
    new_record = Controls(
        id = record_id,
        created_at = current_date,
        fk_patient_id = patient_id,
        fk_patient_nik = patient_data.patient_nik,
        patient_name = patient_data.name,
        last_control = last_control
    )
    db.add(new_record)
    db.commit()
    return patient_id, record_id


def __select_patient_data(patient_nik: str, db: Session):
    patient_list = []
    if patient_nik is None:
        patients = db.query(Patients).all()
        patient_list = []
        for patient in patients:
            _patient = patient.__dict__
            patient_list.append(PatientModel(**_patient))
        return patient_list
    
    patients = db.query(Patients).filter(Patients.nik.contains(patient_nik)).limit(5).all()
    for patient in patients:
        _patient = patient.__dict__
        patient_list.append(PatientModel(**_patient))
    return patient_list

def __select_active_patient_data(db: Session):
    patient_list = []
    patients = db.query(Controls).filter(Controls.classification==None).all()
    for patient in patients:
        patient_list.append(ActivePatientModel(
                                            id=patient.fk_patient_id,
                                            name=patient.patient_name))
    return patient_list


def __update_patient_classification(patient_id:str, diag:str, db: Session):
    curr = datetime.now()
    record = db.query(Controls).where(Controls.fk_patient_id==patient_id and Controls.updated_at==None).order_by(Controls.created_at.desc()).first()
    patient = db.query(Patients).where(Patients.id==patient_id).first();
    if patient:
        patient.classification = diag
        patient.updated_at = curr
        record.classification = diag
        record.updated_at = curr
        db.commit()
        return patient.id
    return None

@records_router.get("/patient", response_model=PatientResponseModel)
def get_patient_data(NIK: str=None, db: Session= Depends(get_db)):
    patient_list = __select_patient_data(NIK, db)
    res = PatientResponseModel(
            code = status.HTTP_200_OK,
            data = patient_list
        )
    return res


@records_router.post("", response_model=RecordCreatedResponseModel, status_code=201)
def create_record(patient_data: CreateRecordRequestModel, db: Session=Depends(get_db)):
    patient_id, record_id = __create_patient(patient_data, db)
    res = RecordCreatedResponseModel(
        code=status.HTTP_201_CREATED,
        data={
            "patient_id": patient_id,
            "record_id": record_id,
        }
    )
    return res


@records_router.get("/{patient_id}")
def get_patient_records(patient_id: str, db: Session=Depends(get_db)):
    validate_uuid(patient_id)
    records = db.execute(text(f"""
                        select p.id as patient_id, p.nik, p."name", c.created_at from patients p
                            join controls c on c.fk_patient_id = p.id
                            where c.fk_patient_id = '{patient_id}';
                        """))
    _records = []
    for row in records:
        _records.append(ControlModel(**row._asdict()))
    res = ControlResponseModel(
        code=status.HTTP_200_OK,
        data=_records
    )
    return res


@records_router.get("/patients/active")
def get_active_patient(db: Session=Depends(get_db)):
    patients = __select_active_patient_data(db)
    res = ActivePatientResponseModel(
            code = status.HTTP_200_OK,
            data = patients
        )
    return res


@records_router.patch("/{patientId}")
def update_patient(patientId: str, req: PatientClassificationRequestModel, db: Session=Depends(get_db)):
    patient_id = __update_patient_classification(patientId, req.classification, db)
    return JSONResponse({"status": "OK"})


def __select_today_records(db: Session):
    start = datetime.combine(date.today(), time.min)
    end = datetime.combine(date.today(), time.max)
    
    controls = db.query(Controls).filter(
        Controls.created_at >= start,
        Controls.created_at <= end
    ).order_by(Controls.created_at.desc()).all()
    
    records = []
    for control in controls:
        records.append(
            ControlModel(
                patient_id=control.fk_patient_id,
                name=control.patient_name,
                nik=control.fk_patient_nik,
                created_at=control.created_at
            )
        )
    return records


@records_router.get("/patients/today")
def get_today_records(db: Session=Depends(get_db)):
    records = __select_today_records(db)
    res = ControlResponseModel(
        code=status.HTTP_200_OK,
        data=records
    )
    return res