from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.queue import (
    QueueTicket
)

from app.models.hospital import (
    
    Hospital
)
from app.models.doctor import Doctor
from app.schemas.queue import (
    QueueCreate,
    QueueStatusUpdate
)

from app.api.deps import (
    require_doctor,
    require_hospital_admin
)

from app.models.user import User

from app.services.websocket_manager import (
    manager
)

router = APIRouter()


# =========================
# JOIN QUEUE
# =========================

@router.post("/")
async def join_queue(
    payload: QueueCreate,
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

    total_queue = db.query(
        QueueTicket
    ).count()

    queue_ticket = QueueTicket(
        patient_name=payload.patient_name,
        doctor_id=payload.doctor_id,
        hospital_id=payload.hospital_id,
        queue_number=total_queue + 1
    )

    db.add(queue_ticket)

    db.commit()

    db.refresh(queue_ticket)

    # LIVE UPDATE
    await manager.broadcast(
        f"New Queue Ticket: {queue_ticket.queue_number}"
    )

    return {
        "message": "Queue joined successfully",
        "ticket": queue_ticket
    }


# =========================
# GET QUEUE
# =========================

@router.get("/")
def get_queue(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hospital_admin
    )
):

    queue = db.query(
        QueueTicket
    ).all()

    return queue


# =========================
# UPDATE QUEUE STATUS
# =========================

@router.patch("/{ticket_id}/status")
async def update_queue_status(
    ticket_id: int,
    payload: QueueStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_doctor
    )
):

    ticket = db.query(
        QueueTicket
    ).filter(
        QueueTicket.id == ticket_id
    ).first()

    if not ticket:

        raise HTTPException(
            status_code=404,
            detail="Queue ticket not found"
        )

    ticket.status = payload.status

    db.commit()

    db.refresh(ticket)

    # LIVE UPDATE
    await manager.broadcast(
        f"Queue {ticket.queue_number} is now {ticket.status}"
    )

    return {
        "message": "Queue updated",
        "ticket": ticket
    }