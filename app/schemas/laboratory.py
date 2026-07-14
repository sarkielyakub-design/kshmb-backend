from pydantic import BaseModel


# =========================
# LAB TEST
# =========================

class LabTestCreate(BaseModel):

    test_name: str
    category: str
    price: float
    description: str


# =========================
# LAB REQUEST
# =========================

class LabRequestCreate(BaseModel):

    patient_id: int
    doctor_id: int
    lab_test_id: int


class LabResultUpdate(BaseModel):

    status: str
    result: str
    technician_notes: str