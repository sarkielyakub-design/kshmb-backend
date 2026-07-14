from typing import Optional

from fastapi import (

    APIRouter,
    Depends,
    HTTPException,
    Query,
    status

)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.doctor import Doctor

from app.models.hospital import (
    Hospital,
    Department
)
from app.models.doctor import Doctor
from app.schemas.doctor import (

    DoctorCreate,
    DoctorUpdate,
    DoctorResponse

)

from app.api.deps import (
    require_hospital_admin
)

from app.models.user import User


router = APIRouter()


# =====================================
# CREATE DOCTOR
# =====================================

@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_doctor(

    payload: DoctorCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    hospital = db.query(Hospital).filter(
        Hospital.id == payload.hospital_id
    ).first()

    if not hospital:

        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    department = db.query(Department).filter(
        Department.id == payload.department_id
    ).first()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    existing = db.query(Doctor).filter(
        Doctor.email == payload.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Doctor already exists"
        )

    doctor = Doctor(**payload.model_dump())

    db.add(doctor)

    db.commit()

    db.refresh(doctor)

    return doctor


# =====================================
# GET DOCTORS
# =====================================

@router.get(
    "/",
    response_model=list[DoctorResponse]
)
def get_doctors(

    db: Session = Depends(get_db),

    hospital_id: Optional[int] = None,

    department_id: Optional[int] = None,

    specialty: Optional[str] = None
):

    query = db.query(Doctor)

    if hospital_id:

        query = query.filter(
            Doctor.hospital_id == hospital_id
        )

    if department_id:

        query = query.filter(
            Doctor.department_id == department_id
        )

    if specialty:

        query = query.filter(
            Doctor.specialty.ilike(
                f"%{specialty}%"
            )
        )

    return query.all()


# =====================================
# GET SINGLE DOCTOR
# =====================================

@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(

    doctor_id: int,

    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor


# =====================================
# UPDATE DOCTOR
# =====================================

@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def update_doctor(

    doctor_id: int,

    payload: DoctorUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(doctor, key, value)

    db.commit()

    db.refresh(doctor)

    return doctor


# =====================================
# DELETE DOCTOR
# =====================================

@router.delete("/{doctor_id}")
def delete_doctor(

    doctor_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    db.delete(doctor)

    db.commit()

    return {
        "message":
        "Doctor deleted successfully"
    }