from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.laboratory import (
    LabTest,
    LabRequest
)

from app.models.patient import (
    Patient
)

from app.models.doctor import Doctor

from app.schemas.laboratory import (
    LabTestCreate,
    LabRequestCreate,
    LabResultUpdate
)

from app.api.deps import (
    require_doctor,
    require_hospital_admin
)

from app.models.user import User

router = APIRouter()


# =========================
# CREATE LAB TEST
# =========================

@router.post("/tests")
def create_lab_test(
    payload: LabTestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    test = LabTest(
        test_name=payload.test_name,
        category=payload.category,
        price=payload.price,
        description=payload.description
    )

    db.add(test)

    db.commit()

    db.refresh(test)

    return test


# =========================
# GET LAB TESTS
# =========================

@router.get("/tests")
def get_lab_tests(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    return db.query(LabTest).all()


# =========================
# CREATE LAB REQUEST
# =========================

@router.post("/requests")
def create_lab_request(
    payload: LabRequestCreate,
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

    test = db.query(LabTest).filter(
        LabTest.id == payload.lab_test_id
    ).first()

    if not test:

        raise HTTPException(
            status_code=404,
            detail="Lab test not found"
        )

    request = LabRequest(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        lab_test_id=payload.lab_test_id
    )

    db.add(request)

    db.commit()

    db.refresh(request)

    return {
        "message": "Lab request created",
        "request": request
    }


# =========================
# UPDATE LAB RESULT
# =========================

@router.patch("/requests/{request_id}")
def update_lab_result(
    request_id: int,
    payload: LabResultUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    request = db.query(
        LabRequest
    ).filter(
        LabRequest.id == request_id
    ).first()

    if not request:

        raise HTTPException(
            status_code=404,
            detail="Lab request not found"
        )

    request.status = payload.status
    request.result = payload.result
    request.technician_notes = payload.technician_notes

    db.commit()

    db.refresh(request)

    return {
        "message": "Lab result updated",
        "request": request
    }


# =========================
# GET LAB REQUESTS
# =========================

@router.get("/requests")
def get_lab_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    return db.query(LabRequest).all()