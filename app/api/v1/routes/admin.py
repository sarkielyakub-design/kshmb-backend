from fastapi import APIRouter, Depends

from app.models.user import User

from app.api.deps import (
    require_super_admin,
    require_hr_admin,
    require_doctor,
    require_hospital_admin
)

router = APIRouter()


# =========================
# SUPER ADMIN DASHBOARD
# =========================

@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(
        require_super_admin
    )
):

    return {
        "message": "Welcome Super Admin",
        "user": current_user.email,
        "role": current_user.role
    }


# =========================
# HR / JOBS MANAGEMENT
# =========================

@router.get("/jobs")
def manage_jobs(
    current_user: User = Depends(
        require_hr_admin
    )
):

    return {
        "message": "HR Recruitment Dashboard",
        "user": current_user.email,
        "permissions": [
            "Create Jobs",
            "Delete Jobs",
            "Review Applications",
            "Shortlist Candidates"
        ]
    }


# =========================
# DOCTOR DASHBOARD
# =========================

@router.get("/doctor")
def doctor_dashboard(
    current_user: User = Depends(
        require_doctor
    )
):

    return {
        "message": "Doctor Dashboard",
        "doctor": current_user.full_name,
        "access": [
            "Patient Records",
            "Appointments",
            "Prescriptions",
            "Medical Reports"
        ]
    }


# =========================
# HOSPITAL ADMIN
# =========================

@router.get("/hospital")
def hospital_dashboard(
    current_user: User = Depends(
        require_hospital_admin
    )
):

    return {
        "message": "Hospital Management Dashboard",
        "admin": current_user.email,
        "features": [
            "Manage Doctors",
            "Manage Nurses",
            "Hospital Reports",
            "Departments",
            "Appointments"
        ]
    }


# =========================
# ANALYTICS
# =========================

@router.get("/analytics")
def analytics_dashboard(
    current_user: User = Depends(
        require_super_admin
    )
):

    return {
        "message": "KSHMB Analytics Dashboard",
        "statistics": {
            "total_hospitals": 25,
            "total_doctors": 320,
            "total_patients": 12500,
            "active_appointments": 412
        }
    }


# =========================
# SYSTEM SETTINGS
# =========================

@router.get("/settings")
def system_settings(
    current_user: User = Depends(
        require_super_admin
    )
):

    return {
        "message": "System Settings Access",
        "settings": [
            "Security",
            "Roles",
            "Database",
            "Notifications",
            "Audit Logs"
        ]
    }