from pydantic import BaseModel


class InvoiceCreate(BaseModel):

    patient_id: int
    service_name: str
    amount: float
    payment_method: str


class PaymentStatusUpdate(BaseModel):

    payment_status: str