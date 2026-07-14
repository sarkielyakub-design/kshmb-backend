from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Time,
    Text
)

from sqlalchemy.orm import relationship

from app.db.session import Base


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # PATIENT INFO
    # =====================================

    patient_name = Column(
        String,
        nullable=False
    )

    patient_email = Column(
        String,
        nullable=False
    )

    patient_phone = Column(
        String,
        nullable=False
    )

    symptoms = Column(
        Text,
        nullable=True
    )

    # =====================================
    # APPOINTMENT INFO
    # =====================================

    appointment_date = Column(
        Date,
        nullable=False
    )

    appointment_time = Column(
        Time,
        nullable=False
    )

    status = Column(
        String,
        default="PENDING"
    )

    queue_number = Column(
        Integer,
        nullable=True
    )

    # =====================================
    # FOREIGN KEYS
    # =====================================

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id")
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    hospital = relationship(
        "Hospital",
        back_populates="appointments"
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments"
    )