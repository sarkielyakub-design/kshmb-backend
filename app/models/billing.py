from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.db.session import Base


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id")
    )

    service_name = Column(String)

    amount = Column(Float)

    payment_status = Column(
        String,
        default="UNPAID"
    )

    payment_method = Column(String)

    invoice_number = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    hospital_id = Column(
    Integer,
    ForeignKey("hospitals.id")
)