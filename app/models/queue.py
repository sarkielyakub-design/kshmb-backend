from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.db.session import Base


class QueueTicket(Base):

    __tablename__ = "queue_tickets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_name = Column(String)

    queue_number = Column(Integer)

    status = Column(
        String,
        default="WAITING"
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )