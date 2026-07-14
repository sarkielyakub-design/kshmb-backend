from pydantic import BaseModel
from datetime import date


# =========================
# MEDICINE
# =========================

class MedicineCreate(BaseModel):

    name: str
    category: str
    manufacturer: str
    supplier: str
    quantity: int
    unit_price: float
    expiry_date: date


# =========================
# PHARMACY SALE
# =========================

class PharmacySaleCreate(BaseModel):

    medicine_id: int
    quantity: int
    patient_name: str