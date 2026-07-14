from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.emergency import (
    Ambulance,
    EmergencyRequest
)

from app.schemas.emergency import (
    AmbulanceCreate,
    EmergencyRequestCreate,
    DispatchAmbulance
)

from app.api.deps import (
    require_hospital_admin
)

from app.models.user import User

from app.services.websocket_manager import (
    manager
)

router = APIRouter()


# =========================
# CREATE AMBULANCE
# =========================

@router.post("/ambulances")
def create_ambulance(
    payload: AmbulanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    ambulance = Ambulance(
        vehicle_number=payload.vehicle_number,
        driver_name=payload.driver_name,
        driver_phone=payload.driver_phone,
        current_location=payload.current_location,
        latitude=payload.latitude,
        longitude=payload.longitude
    )

    db.add(ambulance)

    db.commit()

    db.refresh(ambulance)

    return ambulance


# =========================
# GET AMBULANCES
# =========================

@router.get("/ambulances")
def get_ambulances(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    return db.query(Ambulance).all()


# =========================
# CREATE EMERGENCY REQUEST
# =========================

@router.post("/requests")
async def create_emergency_request(
    payload: EmergencyRequestCreate,
    db: Session = Depends(get_db)
):

    request = EmergencyRequest(
        patient_name=payload.patient_name,
        phone=payload.phone,
        emergency_type=payload.emergency_type,
        pickup_location=payload.pickup_location
    )

    db.add(request)

    db.commit()

    db.refresh(request)

    # REAL-TIME ALERT
    await manager.broadcast(
        f"Emergency Alert: {payload.emergency_type}"
    )

    return {
        "message": "Emergency request created",
        "request": request
    }


# =========================
# DISPATCH AMBULANCE
# =========================

@router.patch("/requests/{request_id}/dispatch")
async def dispatch_ambulance(
    request_id: int,
    payload: DispatchAmbulance,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    request = db.query(
        EmergencyRequest
    ).filter(
        EmergencyRequest.id == request_id
    ).first()

    if not request:

        raise HTTPException(
            status_code=404,
            detail="Emergency request not found"
        )

    ambulance = db.query(
        Ambulance
    ).filter(
        Ambulance.id == payload.ambulance_id
    ).first()

    if not ambulance:

        raise HTTPException(
            status_code=404,
            detail="Ambulance not found"
        )

    ambulance.status = "BUSY"

    request.ambulance_id = payload.ambulance_id

    request.status = payload.status

    db.commit()

    db.refresh(request)

    # REAL-TIME ALERT
    await manager.broadcast(
        f"Ambulance dispatched to {request.patient_name}"
    )

    return {
        "message": "Ambulance dispatched",
        "request": request
    }


# =========================
# GET EMERGENCY REQUESTS
# =========================

@router.get("/requests")
def get_emergency_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    return db.query(EmergencyRequest).all()