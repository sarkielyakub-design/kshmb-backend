from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.api.deps import (
    require_super_admin
)

from app.models.user import User

from app.models.hospital import (
    Hospital,
    
    Department
)

from app.models.doctor import Doctor
from app.models.patient import (
    Patient
)

from app.models.appointment import (
    Appointment
)

from app.models.emergency import (
    Ambulance,
    EmergencyRequest
)

from app.models.recruitment import (
    Job,
    JobApplication
)

from app.models.pharmacy import (
    Medicine
)

from app.models.laboratory import (
    LabRequest
)

router = APIRouter()


# =====================================
# ANALYTICS DASHBOARD
# =====================================

@router.get("/")
def analytics_dashboard(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_super_admin
    )
):

    return {

        "message":
            "KSHMB Analytics Dashboard",

        "statistics": {

            "total_hospitals":
                db.query(Hospital).count(),

            "total_doctors":
                db.query(Doctor).count(),

            "total_departments":
                db.query(Department).count(),

            "total_patients":
                db.query(Patient).count(),

            "total_appointments":
                db.query(Appointment).count(),

            "total_ambulances":
                db.query(Ambulance).count(),

            "total_emergencies":
                db.query(EmergencyRequest).count(),

            "total_jobs":
                db.query(Job).count(),

            "total_job_applications":
                db.query(JobApplication).count(),

            "total_medicines":
                db.query(Medicine).count(),

            "total_lab_requests":
                db.query(LabRequest).count(),
        }
    }