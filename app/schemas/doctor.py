from pydantic import BaseModel
from typing import Optional


# =====================================================
# CREATE
# =====================================================

class DoctorCreate(BaseModel):

    full_name: str

    specialty: str

    phone: str

    email: str

    hospital_id: int

    department_id: int

    # =====================================
    # PROFESSIONAL DATA
    # =====================================

    experience: Optional[str] = None

    qualification: Optional[str] = None

    availability: Optional[str] = None

    bio: Optional[str] = None

    image: Optional[str] = None


# =====================================================
# UPDATE
# =====================================================

class DoctorUpdate(BaseModel):

    full_name: Optional[str] = None

    specialty: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    hospital_id: Optional[int] = None

    department_id: Optional[int] = None

    # =====================================
    # PROFESSIONAL DATA
    # =====================================

    experience: Optional[str] = None

    qualification: Optional[str] = None

    availability: Optional[str] = None

    bio: Optional[str] = None

    image: Optional[str] = None


# =====================================================
# RESPONSE
# =====================================================

class DoctorResponse(BaseModel):

    id: int

    full_name: str

    specialty: str

    phone: str

    email: str

    hospital_id: int

    department_id: int

    # =====================================
    # PROFESSIONAL DATA
    # =====================================

    experience: Optional[str] = None

    qualification: Optional[str] = None

    availability: Optional[str] = None

    bio: Optional[str] = None

    image: Optional[str] = None

    # =====================================
    # ANALYTICS
    # =====================================

    attended_patients: int = 0

    completed_appointments: int = 0

    class Config:

        from_attributes = True