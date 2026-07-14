from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine

# =========================================
# MODELS
# =========================================
from app.models.news import News
from app.models.user import User
from app.models.audit import AuditLog

from app.models.ai_assistant import (
    AIConsultation
)

from app.models.emergency import (
    Ambulance,
    EmergencyRequest
)

from app.models.laboratory import (
    LabTest,
    LabRequest
)

from app.models.pharmacy import (
    Medicine,
    PharmacySale
)
from app.api.v1.routes import ws
from app.models.billing import Invoice

from app.models.queue import QueueTicket

from app.models.notification import Notification

from app.models.patient import (
    Patient,
    MedicalRecord
)

from app.models.appointment import Appointment

from app.models.hospital import (
    Hospital,
    Department,
)
from app.models.doctor import Doctor
from app.models.recruitment import (
    Job,
    JobApplication
)

# =========================================
# ROUTES
# =========================================

from app.api.v1.routes import (
    auth,
    admin,
    hospitals,
    patient,
    medical_record,
    recruitment,
    upload,
    appointment,
    analytics,
    notification,
    queue,
    billing,
    pharmacy,
    laboratory,
    emergency,
    ai_assistant,
    audit,
    doctor,
    staff,
    bedspace,
    news
)

# =========================================
# CREATE DATABASE TABLES
# =========================================

Base.metadata.create_all(bind=engine)

# =========================================
# FASTAPI APP
# =========================================

app = FastAPI(
    title="KSHMB API",
    version="1.0.0",
)

# =========================================
# CORS
# =========================================

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",

        "https://kshmb-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# =========================================
# ROUTERS
# =========================================

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["Admin"]
)

app.include_router(
    hospitals.router,
    prefix="/api/v1/hospitals",
    tags=["Hospitals"]
)

app.include_router(
    patient.router,
    prefix="/api/v1/patients",
    tags=["Patients"]
)

app.include_router(
    recruitment.router,
    prefix="/api/v1/recruitment",
    tags=["Recruitment"]
)

app.include_router(
    upload.router,
    prefix="/api/v1/upload",
    tags=["Upload"]
)

app.include_router(
    appointment.router,
    prefix="/api/v1/appointments",
    tags=["Appointments"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["Analytics"]
)

app.include_router(
    notification.router,
    prefix="/api/v1/notifications",
    tags=["Notifications"]
)

app.include_router(
    queue.router,
    prefix="/api/v1/queue",
    tags=["Queue"]
)

app.include_router(
    billing.router,
    prefix="/api/v1/billing",
    tags=["Billing"]
)

app.include_router(
    pharmacy.router,
    prefix="/api/v1/pharmacy",
    tags=["Pharmacy"]
)

app.include_router(
    laboratory.router,
    prefix="/api/v1/laboratory",
    tags=["Laboratory"]
)

app.include_router(
    emergency.router,
    prefix="/api/v1/emergency",
    tags=["Emergency"]
)

app.include_router(
    ai_assistant.router,
    prefix="/api/v1/ai",
    tags=["AI Medical Assistant"]
)

app.include_router(
    audit.router,
    prefix="/api/v1/audit",
    tags=["Audit"]
)
app.include_router(
    doctor.router,
    prefix="/api/v1/doctors",
    tags=["Doctors"]
)
app.include_router(
    ws.router,
    prefix="/ws",
    tags=["WebSocket"]
)
app.include_router(
    medical_record.router,
    prefix="/api/v1/medical-records",
    tags=["Medical Records"]
)
app.include_router(
    staff.router,
    prefix="/api/v1/staff",
    tags=["Staff"]
)

app.include_router(
    bedspace.router,
    prefix="/api/v1/bedspaces",
    tags=["Bedspaces"]
)
app.include_router(
    news.router,
    prefix="/api/v1/news",
    tags=["News"]
)
# =========================================
# ROOT
# =========================================

@app.get("/")
def home():
    return {
        "message": "KSHMB Backend Running"
    }