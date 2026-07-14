from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =====================================
# CREATE STAFF
# =====================================

class StaffCreate(BaseModel):

    full_name: str

    email: Optional[str] = None

    phone: str

    role: str

    department: Optional[str] = None

    shift: Optional[str] = None

    status: Optional[str] = "ACTIVE"

    hospital_id: int


# =====================================
# UPDATE STAFF
# =====================================

class StaffUpdate(BaseModel):

    full_name: Optional[str] = None

    email: Optional[str] = None

    phone: Optional[str] = None

    role: Optional[str] = None

    department: Optional[str] = None

    shift: Optional[str] = None

    status: Optional[str] = None

    hospital_id: Optional[int] = None


# =====================================
# RESPONSE
# =====================================

class StaffResponse(BaseModel):

    id: int

    full_name: str

    email: Optional[str] = None

    phone: str

    role: str

    department: Optional[str] = None

    shift: Optional[str] = None

    status: Optional[str] = "ACTIVE"

    hospital_id: Optional[int] = None

    created_at: datetime

    class Config:

        from_attributes = True