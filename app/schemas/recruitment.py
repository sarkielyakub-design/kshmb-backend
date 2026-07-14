from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =====================================================
# JOBS
# =====================================================

class JobCreate(BaseModel):

    title: str

    department: str

    location: str

    employment_type: str

    hospital_name: Optional[str] = None

    salary_range: Optional[str] = None

    experience_level: Optional[str] = None

    description: str

    requirements: str

    responsibilities: Optional[str] = None

    deadline: Optional[str] = None


class JobUpdate(BaseModel):

    title: Optional[str] = None

    department: Optional[str] = None

    location: Optional[str] = None

    employment_type: Optional[str] = None

    hospital_name: Optional[str] = None

    salary_range: Optional[str] = None

    experience_level: Optional[str] = None

    description: Optional[str] = None

    requirements: Optional[str] = None

    responsibilities: Optional[str] = None

    status: Optional[str] = None

    deadline: Optional[str] = None


class JobResponse(BaseModel):

    id: int

    title: str

    department: str

    location: str

    employment_type: str

    hospital_name: Optional[str]

    salary_range: Optional[str]

    experience_level: Optional[str]

    description: str

    requirements: str

    responsibilities: Optional[str]

    status: str

    deadline: Optional[str]

    created_at: datetime

    class Config:

        from_attributes = True


# =====================================================
# APPLICATIONS
# =====================================================

class JobApplicationCreate(BaseModel):

    full_name: str

    email: str

    phone: str

    cv_url: str

    address: Optional[str] = None

    qualification: Optional[str] = None

    years_of_experience: Optional[str] = None

    cover_letter: Optional[str] = None


class JobApplicationUpdate(BaseModel):

    status: Optional[str] = None


class JobApplicationResponse(BaseModel):

    id: int

    full_name: str

    email: str

    phone: str

    address: Optional[str]

    qualification: Optional[str]

    years_of_experience: Optional[str]

    cv_url: str

    cover_letter: Optional[str]

    status: str

    job_id: int

    created_at: datetime

    # RELATIONSHIP

    job: Optional[JobResponse] = None

    class Config:

        from_attributes = True