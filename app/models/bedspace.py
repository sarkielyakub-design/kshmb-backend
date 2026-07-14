from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.db.session import Base


class BedSpace(Base):

    __tablename__ = "bed_spaces"

    # =====================================
    # PRIMARY KEY
    # =====================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # BED INFO
    # =====================================

    ward_name = Column(
        String,
        nullable=False
    )

    bed_number = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=True
    )

    occupied = Column(
        Boolean,
        default=False
    )

    patient_name = Column(
        String,
        nullable=True
    )

    # =====================================
    # HOSPITAL RELATION
    # =====================================

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id"),
        nullable=False
    )

    hospital = relationship(
        "Hospital",
        back_populates="bed_spaces"
    )

    # =====================================
    # TIMESTAMP
    # =====================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )