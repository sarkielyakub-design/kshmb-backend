from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.db.session import Base


# =========================
# LAB TEST
# =========================

class LabTest(Base):

    __tablename__ = "lab_tests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    test_name = Column(String)

    category = Column(String)

    price = Column(Float)

    description = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================
# LAB REQUEST
# =========================

class LabRequest(Base):

    __tablename__ = "lab_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id")
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )

    lab_test_id = Column(
        Integer,
        ForeignKey("lab_tests.id")
    )

    status = Column(
        String,
        default="PENDING"
    )

    result = Column(Text)

    technician_notes = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    hospital_id = Column(
    Integer,
    ForeignKey("hospitals.id")
)