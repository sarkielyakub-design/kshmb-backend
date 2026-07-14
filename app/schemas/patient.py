from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =====================================================
# PATIENT
# =====================================================

class PatientCreate(BaseModel):

    full_name: str

    email: Optional[str] = None

    phone: str

    gender: str

    blood_group: Optional[str] = None

    address: Optional[str] = None

    emergency_contact: Optional[str] = None

    age: Optional[int] = None


class PatientResponse(BaseModel):

    id: int

    full_name: str

    email: Optional[str]

    phone: str

    gender: str

    blood_group: Optional[str]

    address: Optional[str]

    emergency_contact: Optional[str]

    age: Optional[int]

    patient_number: Optional[str]

    created_at: datetime

    class Config:

        from_attributes = True


# =====================================================
# MEDICAL RECORD
# =====================================================

class MedicalRecordCreate(BaseModel):

    diagnosis: Optional[str] = None

    symptoms: Optional[str] = None

    prescription: Optional[str] = None

    doctor_notes: Optional[str] = None

    lab_results: Optional[str] = None

    patient_id: int

    doctor_id: int


class MedicalRecordResponse(BaseModel):

    id: int

    diagnosis: Optional[str]

    symptoms: Optional[str]

    prescription: Optional[str]

    doctor_notes: Optional[str]

    lab_results: Optional[str]

    patient_id: int

    doctor_id: int

    visit_date: datetime

    class Config:

        from_attributes = True