from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.hospital import (
    Hospital,
    Department
)

from app.models.doctor import Doctor
from app.models.staff import Staff
from app.models.bedspace import BedSpace

from app.schemas.hospital import (
    HospitalCreate,
    HospitalResponse,
    DepartmentCreate,
    DepartmentResponse,
    DoctorCreate,
    DoctorResponse
)

from app.api.deps import (
    require_hospital_admin,
    require_super_admin
)

from app.models.user import User

router = APIRouter()

# =====================================================
# CREATE HOSPITAL
# =====================================================

@router.post(
    "/",
    response_model=HospitalResponse,
    status_code=status.HTTP_201_CREATED
)
def create_hospital(
    payload: HospitalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):

    existing = db.query(Hospital).filter(
        Hospital.name == payload.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Hospital already exists"
        )

    hospital = Hospital(
        name=payload.name.strip(),
        address=payload.address.strip(),
        phone=payload.phone.strip(),
        lga=payload.lga.strip(),
        hospital_type=payload.hospital_type.strip(),
        bed_space=payload.bed_space,
        annual_patients=payload.annual_patients,
        total_staff=payload.total_staff,
        emergency_units=payload.emergency_units,
        image=payload.image,
        description=payload.description
    )

    db.add(hospital)

    db.commit()

    db.refresh(hospital)

    return hospital


# =====================================================
# GET ALL HOSPITALS
# =====================================================

@router.get("/")
def get_hospitals(
    db: Session = Depends(get_db),
    search: Optional[str] = None
):

    query = db.query(Hospital)

    if search:
        query = query.filter(
            Hospital.name.ilike(f"%{search}%")
        )

    hospitals = query.all()

    results = []

    for hospital in hospitals:

        total_staff = db.query(Staff).filter(
            Staff.hospital_id == hospital.id
        ).count()

        total_doctors = db.query(Doctor).filter(
            Doctor.hospital_id == hospital.id
        ).count()

        total_bedspaces = db.query(BedSpace).filter(
            BedSpace.hospital_id == hospital.id
        ).count()

        occupied_beds = db.query(BedSpace).filter(
            BedSpace.hospital_id == hospital.id,
            BedSpace.occupied == True
        ).count()

        results.append({
            "id": hospital.id,
            "name": hospital.name,
            "hospital_type": hospital.hospital_type,
            "address": hospital.address,
            "phone": hospital.phone,
            "lga": hospital.lga,
            "annual_patients": hospital.annual_patients,
            "total_staff": total_staff,
            "total_doctors": total_doctors,
            "total_bedspaces": total_bedspaces,
            "occupied_beds": occupied_beds,
            "available_beds": total_bedspaces - occupied_beds,
            "image": hospital.image,
            "description": hospital.description
        })

    return results


# =====================================================
# CREATE DEPARTMENT
# =====================================================

@router.post(
    "/departments",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hospital_admin)
):

    hospital = db.query(Hospital).filter(
        Hospital.id == payload.hospital_id
    ).first()

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    department = Department(
        name=payload.name.strip(),
        description=payload.description,
        hospital_id=payload.hospital_id
    )

    db.add(department)

    db.commit()

    db.refresh(department)

    return department


# =====================================================
# GET DEPARTMENTS
# =====================================================

@router.get("/departments/{hospital_id}")
def get_departments(
    hospital_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Department).filter(
        Department.hospital_id == hospital_id
    ).all()


# =====================================================
# CREATE DOCTOR
# =====================================================

@router.post(
    "/doctors",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_doctor(
    payload: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hospital_admin)
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
            detail="Doctor email already exists"
        )

    doctor = Doctor(
        full_name=payload.full_name,
        specialty=payload.specialty,
        phone=payload.phone,
        email=payload.email,
        experience=payload.experience,
        qualification=payload.qualification,
        availability=payload.availability,
        bio=payload.bio,
        image=payload.image,
        hospital_id=payload.hospital_id,
        department_id=payload.department_id
    )

    db.add(doctor)

    db.commit()

    db.refresh(doctor)

    return doctor


# =====================================================
# GET ALL DOCTORS
# IMPORTANT: BEFORE /{hospital_id}
# =====================================================

@router.get(
    "/doctors",
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


# =====================================================
# GET SINGLE DOCTOR
# =====================================================

@router.get(
    "/doctors/{doctor_id}",
    response_model=DoctorResponse
)
def get_single_doctor(
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


# =====================================================
# DELETE DOCTOR
# =====================================================

@router.delete("/doctors/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hospital_admin)
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
        "message": "Doctor deleted successfully"
    }


# =====================================================
# GET SINGLE HOSPITAL
# KEEP LAST
# =====================================================

@router.get("/{hospital_id}")
def get_single_hospital(
    hospital_id: int,
    db: Session = Depends(get_db)
):

    hospital = db.query(Hospital).filter(
        Hospital.id == hospital_id
    ).first()

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    return hospital


# =====================================================
# DELETE HOSPITAL
# =====================================================

@router.delete("/{hospital_id}")
def delete_hospital(
    hospital_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):

    hospital = db.query(Hospital).filter(
        Hospital.id == hospital_id
    ).first()

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    db.delete(hospital)

    db.commit()

    return {
        "message": "Hospital deleted successfully"
    }