from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.db.session import Base


# =====================================================
# JOB
# =====================================================

class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # BASIC INFO
    # =====================================

    title = Column(
        String,
        nullable=False
    )

    department = Column(
        String,
        nullable=False
    )

    location = Column(
        String,
        nullable=False
    )

    employment_type = Column(
        String,
        nullable=False
    )

    hospital_name = Column(
        String,
        nullable=True
    )

    # =====================================
    # PROFESSIONAL DATA
    # =====================================

    salary_range = Column(
        String,
        nullable=True
    )

    experience_level = Column(
        String,
        nullable=True
    )

    # =====================================
    # CONTENT
    # =====================================

    description = Column(
        Text,
        nullable=False
    )

    requirements = Column(
        Text,
        nullable=False
    )

    responsibilities = Column(
        Text,
        nullable=True
    )

    # =====================================
    # STATUS
    # =====================================

    status = Column(
        String,
        default="OPEN"
    )

    deadline = Column(
        String,
        nullable=True
    )

    # =====================================
    # TIMESTAMP
    # =====================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================
    # RELATIONSHIP
    # =====================================

    applications = relationship(

        "JobApplication",

        back_populates="job",

        cascade="all, delete-orphan"
    )


# =====================================================
# JOB APPLICATION
# =====================================================

class JobApplication(Base):

    __tablename__ = "job_applications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # APPLICANT INFO
    # =====================================

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=False
    )

    address = Column(
        String,
        nullable=True
    )

    qualification = Column(
        String,
        nullable=True
    )

    years_of_experience = Column(
        String,
        nullable=True
    )

    # =====================================
    # FILES
    # =====================================

    cv_url = Column(
        String,
        nullable=False
    )

    cover_letter = Column(
        Text,
        nullable=True
    )

    # =====================================
    # STATUS
    # =====================================

    status = Column(
        String,
        default="PENDING"
    )

    # =====================================
    # FOREIGN KEY
    # =====================================

    job_id = Column(
        Integer,
        ForeignKey("jobs.id")
    )

    # =====================================
    # TIMESTAMP
    # =====================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =====================================
    # RELATIONSHIP
    # =====================================

    job = relationship(

        "Job",

        back_populates="applications"
    )