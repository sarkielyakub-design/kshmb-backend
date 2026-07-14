from pydantic import BaseModel


class QueueCreate(BaseModel):

    patient_name: str
    doctor_id: int
    hospital_id: int


class QueueStatusUpdate(BaseModel):

    status: str