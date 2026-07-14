from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.appointment import (
    Appointment
)

from app.models.hospital import (
    
    Hospital
)
from app.models.doctor import Doctor
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentStatusUpdate
)

from app.api.deps import (
    require_doctor,
    require_hospital_admin
)

from app.models.user import User

router = APIRouter()


# =========================
# BOOK APPOINTMENT
# =========================

@router.post("/")
def book_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == payload.doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    hospital = db.query(Hospital).filter(
        Hospital.id == payload.hospital_id
    ).first()

    if not hospital:

        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    total_appointments = db.query(
        Appointment
    ).count()

    appointment = Appointment(

        patient_name=payload.patient_name,

        patient_email=payload.patient_email,

        patient_phone=payload.patient_phone,

        symptoms=payload.symptoms,

        appointment_date=payload.appointment_date,

        appointment_time=payload.appointment_time,

        doctor_id=payload.doctor_id,

        hospital_id=payload.hospital_id,

        queue_number=total_appointments + 1,

        status="PENDING"
    )

    db.add(appointment)

    db.commit()

    db.refresh(appointment)

    return {

        "message":
            "Appointment booked successfully",

        "appointment":
            appointment
    }


# =========================
# GET ALL APPOINTMENTS
# =========================

@router.get("/")
def get_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    appointments = db.query(
        Appointment
    ).all()

    return appointments


# =========================
# GET DOCTOR APPOINTMENTS
# =========================

@router.get("/doctor")
def get_doctor_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_doctor
    )
):

    doctor = db.query(Doctor).filter(
        Doctor.email == current_user.email
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor profile not found"
        )

    appointments = db.query(
        Appointment
    ).filter(
        Appointment.doctor_id == doctor.id
    ).all()

    return appointments


# =========================
# UPDATE STATUS
# =========================

@router.patch("/{appointment_id}/status")
def update_status(
    appointment_id: int,
    payload: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_doctor
    )
):

    appointment = db.query(
        Appointment
    ).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.status = payload.status

    db.commit()

    db.refresh(appointment)

    return {

        "message":
            "Appointment updated successfully",

        "appointment":
            appointment
    }


# =========================
# DELETE APPOINTMENT
# =========================

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    appointment = db.query(
        Appointment
    ).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)

    db.commit()

    return {
        "message":
            "Appointment deleted successfully"
    }