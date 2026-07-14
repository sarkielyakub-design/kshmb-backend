import random

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.patient import (
    Patient,
    MedicalRecord
)

from app.models.doctor import Doctor

from app.schemas.patient import (
    PatientCreate,
    MedicalRecordCreate
)

from app.api.deps import (
    require_doctor,
    require_hospital_admin
)

from app.models.user import User

router = APIRouter()


# =====================================================
# CREATE PATIENT
# =====================================================

@router.post("/")
def create_patient(
    payload: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    patient = Patient(

        full_name=payload.full_name,

        email=payload.email,

        phone=payload.phone,

        gender=payload.gender,

        blood_group=payload.blood_group,

        address=payload.address,

        emergency_contact=payload.emergency_contact,

        age=payload.age,

        patient_number=f"KSHMB-{random.randint(10000,99999)}"
    )

    db.add(patient)

    db.commit()

    db.refresh(patient)

    return {
        "message": "Patient created successfully",
        "patient": patient
    }


# =====================================================
# GET PATIENTS
# =====================================================

@router.get("/")
def get_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    patients = db.query(Patient).all()

    return patients


# =====================================================
# GET SINGLE PATIENT
# =====================================================

@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# =====================================================
# CREATE MEDICAL RECORD
# =====================================================

@router.post("/records")
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
        "message": "Medical record created successfully",
        "record": record
    }


# =====================================================
# GET PATIENT RECORDS
# =====================================================

@router.get("/{patient_id}/records")
def get_patient_records(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_doctor
    )
):

    records = db.query(
        MedicalRecord
    ).filter(
        MedicalRecord.patient_id == patient_id
    ).all()

    result = []

    for record in records:

        patient = db.query(Patient).filter(
            Patient.id == record.patient_id
        ).first()

        doctor = db.query(Doctor).filter(
            Doctor.id == record.doctor_id
        ).first()

        result.append({

            "id": record.id,

            "diagnosis": record.diagnosis,

            "symptoms": record.symptoms,

            "prescription": record.prescription,

            "doctor_notes": record.doctor_notes,

            "lab_results": record.lab_results,

            "visit_date": record.visit_date,

            "patient_id": record.patient_id,

            "doctor_id": record.doctor_id,

            # CONNECTED DATA
            "patient_name": patient.full_name if patient else None,

            "doctor_name": doctor.full_name if doctor else None,
        })

    return result