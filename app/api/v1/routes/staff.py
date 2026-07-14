from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.staff import Staff

from app.models.hospital import Hospital

from app.schemas.staff import (
    StaffCreate,
    StaffResponse
)

from app.api.deps import (
    require_hospital_admin
)

from app.models.user import User


router = APIRouter()


# =====================================
# CREATE STAFF
# =====================================

@router.post(
    "/",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED
)
def create_staff(

    payload: StaffCreate,

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

    staff = Staff(

        full_name=payload.full_name,

        role=payload.role,

        phone=payload.phone,

        email=payload.email,

        department=payload.department,

        shift=payload.shift,

        status="ACTIVE",

        hospital_id=payload.hospital_id
    )

    db.add(staff)

    db.commit()

    db.refresh(staff)

    return staff


# =====================================
# GET ALL STAFF
# =====================================

@router.get(
    "/",
    response_model=list[StaffResponse]
)
def get_staff(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    return db.query(Staff).all()


# =====================================
# GET HOSPITAL STAFF
# =====================================

@router.get(
    "/hospital/{hospital_id}",
    response_model=list[StaffResponse]
)
def get_hospital_staff(

    hospital_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    hospital = db.query(Hospital).filter(
        Hospital.id == hospital_id
    ).first()

    if not hospital:

        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    return db.query(Staff).filter(
        Staff.hospital_id == hospital_id
    ).all()


# =====================================
# GET SINGLE STAFF
# =====================================

@router.get(
    "/{staff_id}",
    response_model=StaffResponse
)
def get_single_staff(

    staff_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    staff = db.query(Staff).filter(
        Staff.id == staff_id
    ).first()

    if not staff:

        raise HTTPException(
            status_code=404,
            detail="Staff not found"
        )

    return staff


# =====================================
# DELETE STAFF
# =====================================

@router.delete(
    "/{staff_id}"
)
def delete_staff(

    staff_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    staff = db.query(Staff).filter(
        Staff.id == staff_id
    ).first()

    if not staff:

        raise HTTPException(
            status_code=404,
            detail="Staff not found"
        )

    db.delete(staff)

    db.commit()

    return {
        "message": "Staff deleted successfully"
    }