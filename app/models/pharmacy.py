from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.db.session import Base


# =========================
# MEDICINE
# =========================

class Medicine(Base):

    __tablename__ = "medicines"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    category = Column(String)

    manufacturer = Column(String)

    supplier = Column(String)

    quantity = Column(Integer)

    unit_price = Column(Float)

    expiry_date = Column(Date)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =========================
# PHARMACY SALE
# =========================

class PharmacySale(Base):

    __tablename__ = "pharmacy_sales"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    medicine_name = Column(String)

    quantity = Column(Integer)

    total_price = Column(Float)

    patient_name = Column(String)

    sold_by = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    hospital_id = Column(
    Integer,
    ForeignKey("hospitals.id")
)