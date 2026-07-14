from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.db.session import Base


class Staff(Base):

    __tablename__ = "staff"

    # =====================================
    # PRIMARY KEY
    # =====================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================
    # STAFF INFO
    # =====================================

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=True,
        unique=True
    )

    phone = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False
    )

    department = Column(
        String,
        nullable=True
    )

    shift = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        default="ACTIVE"
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
        back_populates="staff"
    )

    # =====================================
    # TIMESTAMP
    # =====================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )