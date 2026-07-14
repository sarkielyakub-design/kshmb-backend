from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =====================================
# CREATE BEDSPACE
# =====================================

class BedSpaceCreate(BaseModel):

    ward_name: str

    bed_number: str

    category: Optional[str] = None

    occupied: bool = False

    patient_name: Optional[str] = None

    hospital_id: int


# =====================================
# UPDATE BEDSPACE
# =====================================

class BedSpaceUpdate(BaseModel):

    ward_name: Optional[str] = None

    bed_number: Optional[str] = None

    category: Optional[str] = None

    occupied: Optional[bool] = None

    patient_name: Optional[str] = None


# =====================================
# RESPONSE
# =====================================

class BedSpaceResponse(BaseModel):

    id: int

    ward_name: str

    bed_number: str

    category: Optional[str]

    occupied: bool

    patient_name: Optional[str]

    hospital_id: int

    created_at: datetime

    class Config:

        from_attributes = True