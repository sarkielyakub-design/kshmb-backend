from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from app.db.session import Base


# =====================================================
# DOCTOR
# =====================================================

class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # BASIC INFO
    # =====================================================

    full_name = Column(
        String,
        nullable=False
    )

    specialty = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    # =====================================================
    # PROFESSIONAL DATA
    # =====================================================

    experience = Column(
        String,
        nullable=True
    )

    qualification = Column(
        String,
        nullable=True
    )

    availability = Column(
        String,
        nullable=True
    )

    bio = Column(
        Text,
        nullable=True
    )

    image = Column(
        String,
        nullable=True
    )

    # =====================================================
    # ANALYTICS
    # =====================================================

    attended_patients = Column(
        Integer,
        default=0
    )

    completed_appointments = Column(
        Integer,
        default=0
    )

    # =====================================================
    # FOREIGN KEYS
    # =====================================================

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id"),
        nullable=False
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    hospital = relationship(
        "Hospital",
        back_populates="doctors"
    )

    department = relationship(
        "Department",
        back_populates="doctors"
    )

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )
    medical_records = relationship(
    "MedicalRecord",
    back_populates="doctor",
    cascade="all, delete-orphan"
)