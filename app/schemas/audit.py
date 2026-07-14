from pydantic import BaseModel
from datetime import datetime


# =========================
# AUDIT RESPONSE
# =========================

class AuditLogResponse(BaseModel):

    id: int

    user_email: str

    action: str

    module: str

    ip_address: str

    description: str

    created_at: datetime

    class Config:

        from_attributes = True