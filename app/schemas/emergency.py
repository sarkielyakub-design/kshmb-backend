from pydantic import BaseModel


# =========================
# AMBULANCE
# =========================

class AmbulanceCreate(BaseModel):

    vehicle_number: str
    driver_name: str
    driver_phone: str
    current_location: str
    latitude: float
    longitude: float


# =========================
# EMERGENCY REQUEST
# =========================

class EmergencyRequestCreate(BaseModel):

    patient_name: str
    phone: str
    emergency_type: str
    pickup_location: str


class DispatchAmbulance(BaseModel):

    ambulance_id: int
    status: str