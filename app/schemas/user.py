from pydantic import BaseModel, EmailStr
from typing import Optional


# =========================================
# REGISTER
# =========================================

class UserCreate(BaseModel):

    full_name: str

    email: EmailStr

    password: str

    role: Optional[str] = "PATIENT"

    hospital_id: Optional[int] = None


# =========================================
# LOGIN
# =========================================

class UserLogin(BaseModel):

    email: EmailStr

    password: str