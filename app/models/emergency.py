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


# =========================
# AMBULANCE
# =========================

class Ambulance(Base):

    __tablename__ = "ambulances"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_number = Column(String)

    driver_name = Column(String)

    driver_phone = Column(String)

    current_location = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)

    status = Column(
        String,
        default="AVAILABLE"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================
# EMERGENCY REQUEST
# =========================

class EmergencyRequest(Base):

    __tablename__ = "emergency_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_name = Column(String)

    phone = Column(String)

    emergency_type = Column(String)

    pickup_location = Column(String)

    status = Column(
        String,
        default="PENDING"
    )

    ambulance_id = Column(
        Integer,
        ForeignKey("ambulances.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )