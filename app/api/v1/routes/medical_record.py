from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.patient import (
    MedicalRecord,
    Patient
)

from app.models.doctor import Doctor

from app.schemas.patient import (
    MedicalRecordCreate
)

from app.api.deps import (
    require_doctor
)

from app.models.user import User

router = APIRouter()


# =====================================
# GET ALL MEDICAL RECORDS
# =====================================

@router.get("/")
def get_medical_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_doctor
    )
):

    records = db.query(
        MedicalRecord
    ).all()

    results = []

    for record in records:

        patient = db.query(Patient).filter(
            Patient.id == record.patient_id
        ).first()

        doctor = db.query(Doctor).filter(
            Doctor.id == record.doctor_id
        ).first()

        results.append({

            "id": record.id,

            "patient_id": record.patient_id,

            "patient_name":
                patient.full_name
                if patient else None,

            "doctor_id": record.doctor_id,

            "doctor_name":
                doctor.full_name
                if doctor else None,

            "diagnosis":
                record.diagnosis,

            "symptoms":
                record.symptoms,

            "prescription":
                record.prescription,

            "doctor_notes":
                record.doctor_notes,

            "lab_results":
                record.lab_results,

            "visit_date":
                record.visit_date,
        })

    return results


# =====================================
# GET SINGLE RECORD
# =====================================

@router.get("/{record_id}")
def get_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_doctor
    )
):

    record = db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.id == record_id
    ).first()

    if not record:

        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == record.patient_id
    ).first()

    doctor = db.query(Doctor).filter(
        Doctor.id == record.doctor_id
    ).first()

    return {

        "id": record.id,

        "patient_id": record.patient_id,

        "patient_name":
            patient.full_name
            if patient else None,

        "doctor_id": record.doctor_id,

        "doctor_name":
            doctor.full_name
            if doctor else None,

        "diagnosis":
            record.diagnosis,

        "symptoms":
            record.symptoms,

        "prescription":
            record.prescription,

        "doctor_notes":
            record.doctor_notes,

        "lab_results":
            record.lab_results,

        "visit_date":
            record.visit_date,
    }


# =====================================
# CREATE RECORD
# =====================================

@router.post("/")
def create_medical_record(
    payload: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_doctor
    )
):

    patient = db.query(Patient).filter(
        Patient.id == payload.patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == payload.doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    record = MedicalRecord(

        diagnosis=payload.diagnosis,

        symptoms=payload.symptoms,

        prescription=payload.prescription,

        doctor_notes=payload.doctor_notes,

        lab_results=payload.lab_results,

        patient_id=payload.patient_id,

        doctor_id=payload.doctor_id
    )

    db.add(record)

    db.commit()

    db.refresh(record)

    return {

        "message":
            "Medical record created",

        "record": record
    }