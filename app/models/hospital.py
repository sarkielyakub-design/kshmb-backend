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
# HOSPITAL
# =====================================================

class Hospital(Base):

    __tablename__ = "hospitals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # BASIC INFO
    # =====================================

    name = Column(
        String,
        nullable=False
    )

    address = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=False
    )

    lga = Column(
        String,
        nullable=False
    )

    hospital_type = Column(
        String,
        nullable=False
    )

    # =====================================
    # ANALYTICS
    # =====================================

    bed_space = Column(
        Integer,
        default=0
    )

    annual_patients = Column(
        Integer,
        default=0
    )

    total_staff = Column(
        Integer,
        default=0
    )

    emergency_units = Column(
        Integer,
        default=0
    )

    # =====================================
    # MEDIA
    # =====================================

    image = Column(
        String,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    departments = relationship(

        "Department",

        back_populates="hospital",

        cascade="all, delete-orphan"
    )

    doctors = relationship(

        "Doctor",

        back_populates="hospital",

        cascade="all, delete-orphan"
    )

    appointments = relationship(

        "Appointment",

        back_populates="hospital",

        cascade="all, delete-orphan"
    )

    # =====================================
    # STAFF RELATIONSHIP
    # =====================================

    staff = relationship(

        "Staff",

        back_populates="hospital",

        cascade="all, delete-orphan"
    )

    # =====================================
    # BED SPACE RELATIONSHIP
    # =====================================

    bed_spaces = relationship(

        "BedSpace",

        back_populates="hospital",

        cascade="all, delete-orphan"
    )


# =====================================================
# DEPARTMENT
# =====================================================

class Department(Base):

    __tablename__ = "departments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id")
    )

    # =====================================
    # RELATIONSHIPS
    # =====================================

    hospital = relationship(

        "Hospital",

        back_populates="departments"
    )

    doctors = relationship(

        "Doctor",

        back_populates="department",

        cascade="all, delete-orphan"
    )