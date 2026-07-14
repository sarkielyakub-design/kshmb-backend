from pydantic import BaseModel
from datetime import date, time


class AppointmentCreate(BaseModel):

    patient_name: str
    patient_email: str
    patient_phone: str
    symptoms: str

    appointment_date: date
    appointment_time: time

    doctor_id: int
    hospital_id: int


class AppointmentStatusUpdate(BaseModel):

    status: str