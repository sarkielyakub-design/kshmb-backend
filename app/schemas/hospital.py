from pydantic import BaseModel
from typing import Optional


# ==========================================
# HOSPITAL
# ==========================================

class HospitalCreate(BaseModel):

    name: str

    address: str

    phone: str

    lga: str

    hospital_type: str

    # =====================================
    # ANALYTICS
    # =====================================

    bed_space: int = 0

    annual_patients: int = 0

    total_staff: int = 0

    emergency_units: int = 0

    # =====================================
    # MEDIA
    # =====================================

    image: Optional[str] = None

    description: Optional[str] = None


class HospitalUpdate(BaseModel):

    name: Optional[str] = None

    address: Optional[str] = None

    phone: Optional[str] = None

    lga: Optional[str] = None

    hospital_type: Optional[str] = None

    bed_space: Optional[int] = None

    annual_patients: Optional[int] = None

    total_staff: Optional[int] = None

    emergency_units: Optional[int] = None

    image: Optional[str] = None

    description: Optional[str] = None


class HospitalResponse(HospitalCreate):

    id: int

    class Config:

        from_attributes = True


# ==========================================
# DEPARTMENT
# ==========================================

class DepartmentCreate(BaseModel):

    name: str

    description: Optional[str] = None

    hospital_id: int


class DepartmentUpdate(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None


class DepartmentResponse(DepartmentCreate):

    id: int

    class Config:

        from_attributes = True


# ==========================================
# DOCTOR
# ==========================================

class DoctorCreate(BaseModel):

    full_name: str

    specialty: str

    phone: str

    email: str

    hospital_id: int

    department_id: int

    # =====================================
    # EXTRA DETAILS
    # =====================================

    experience: Optional[str] = None

    qualification: Optional[str] = None

    availability: Optional[str] = None

    image: Optional[str] = None

    bio: Optional[str] = None


class DoctorUpdate(BaseModel):

    full_name: Optional[str] = None

    specialty: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    hospital_id: Optional[int] = None

    department_id: Optional[int] = None

    experience: Optional[str] = None

    qualification: Optional[str] = None

    availability: Optional[str] = None

    image: Optional[str] = None

    bio: Optional[str] = None


class DoctorResponse(DoctorCreate):

    id: int

    class Config:

        from_attributes = True


# ==========================================
# STAFF
# ==========================================

class StaffCreate(BaseModel):

    full_name: str

    email: Optional[str] = None

    phone: str

    role: str

    department: Optional[str] = None

    shift: Optional[str] = None

    status: Optional[str] = "ACTIVE"

    hospital_id: int


class StaffUpdate(BaseModel):

    full_name: Optional[str] = None

    email: Optional[str] = None

    phone: Optional[str] = None

    role: Optional[str] = None

    department: Optional[str] = None

    shift: Optional[str] = None

    status: Optional[str] = None

    hospital_id: Optional[int] = None


class StaffResponse(StaffCreate):

    id: int

    class Config:

        from_attributes = True


# ==========================================
# BED SPACE
# ==========================================

class BedSpaceCreate(BaseModel):

    ward_name: str

    bed_number: str

    category: Optional[str] = None

    occupied: bool = False

    patient_name: Optional[str] = None

    hospital_id: int


class BedSpaceUpdate(BaseModel):

    ward_name: Optional[str] = None

    bed_number: Optional[str] = None

    category: Optional[str] = None

    occupied: Optional[bool] = None

    patient_name: Optional[str] = None

    hospital_id: Optional[int] = None


class BedSpaceResponse(BedSpaceCreate):

    id: int

    class Config:

        from_attributes = True