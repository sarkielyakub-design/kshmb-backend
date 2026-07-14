from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.bedspace import BedSpace

from app.models.hospital import Hospital

from app.schemas.bedspace import (
    BedSpaceCreate,
    BedSpaceResponse
)

from app.api.deps import (
    require_hospital_admin
)

from app.models.user import User


router = APIRouter()


# =====================================
# CREATE BEDSPACE
# =====================================

@router.post(
    "/",
    response_model=BedSpaceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_bedspace(

    payload: BedSpaceCreate,

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

    bedspace = BedSpace(

        ward_name=payload.ward_name,

        bed_number=payload.bed_number,

        category=payload.category,

        occupied=payload.occupied,

        patient_name=payload.patient_name,

        hospital_id=payload.hospital_id
    )

    db.add(bedspace)

    db.commit()

    db.refresh(bedspace)

    return bedspace


# =====================================
# GET ALL BEDSPACES
# =====================================

@router.get(
    "/",
    response_model=list[BedSpaceResponse]
)
def get_bedspaces(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    return db.query(BedSpace).all()


# =====================================
# GET HOSPITAL BEDSPACES
# =====================================

@router.get(
    "/hospital/{hospital_id}",
    response_model=list[BedSpaceResponse]
)
def get_hospital_bedspaces(

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

    return db.query(BedSpace).filter(
        BedSpace.hospital_id == hospital_id
    ).all()


# =====================================
# GET SINGLE BEDSPACE
# =====================================

@router.get(
    "/single/{bedspace_id}",
    response_model=BedSpaceResponse
)
def get_single_bedspace(

    bedspace_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    bedspace = db.query(BedSpace).filter(
        BedSpace.id == bedspace_id
    ).first()

    if not bedspace:

        raise HTTPException(
            status_code=404,
            detail="Bedspace not found"
        )

    return bedspace


# =====================================
# DELETE BEDSPACE
# =====================================

@router.delete(
    "/{bedspace_id}"
)
def delete_bedspace(

    bedspace_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_hospital_admin
    )
):

    bedspace = db.query(BedSpace).filter(
        BedSpace.id == bedspace_id
    ).first()

    if not bedspace:

        raise HTTPException(
            status_code=404,
            detail="Bedspace not found"
        )

    db.delete(bedspace)

    db.commit()

    return {
        "message": "Bedspace deleted successfully"
    }