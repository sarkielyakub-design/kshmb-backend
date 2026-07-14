from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.db.session import Base


# =====================================================
# PATIENT
# =====================================================

class Patient(Base):

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=True
    )

    phone = Column(
        String,
        nullable=False
    )

    gender = Column(
        String,
        nullable=False
    )

    blood_group = Column(
        String,
        nullable=True
    )

    address = Column(
        Text,
        nullable=True
    )

    emergency_contact = Column(
        String,
        nullable=True
    )

    age = Column(
        Integer,
        nullable=True
    )

    patient_number = Column(
        String,
        unique=True,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================
    # RELATIONSHIP
    # =====================================

    medical_records = relationship(
        "MedicalRecord",
        back_populates="patient",
        cascade="all, delete-orphan"
    )


# =====================================================
# MEDICAL RECORD
# =====================================================

class MedicalRecord(Base):

    __tablename__ = "medical_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    diagnosis = Column(
        Text,
        nullable=True
    )

    symptoms = Column(
        Text,
        nullable=True
    )

    prescription = Column(
        Text,
        nullable=True
    )

    doctor_notes = Column(
        Text,
        nullable=True
    )

    lab_results = Column(
        Text,
        nullable=True
    )

    visit_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================
    # FOREIGN KEYS
    # =====================================

    patient_id = Column(
        Integer,
        ForeignKey("patients.id")
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )

    # =====================================
    # RELATIONSHIP
    # =====================================

    patient = relationship(
        "Patient",
        back_populates="medical_records"
    )

    doctor = relationship(
        "Doctor",
        back_populates="medical_records"
    )