from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query
)

from typing import Optional

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.recruitment import (
    Job,
    JobApplication
)

from app.models.hospital import Hospital

from app.schemas.recruitment import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobApplicationCreate,
    JobApplicationResponse
)

from app.api.deps import (
    require_hr_admin
)

from app.models.user import User

router = APIRouter()


# =====================================================
# CREATE JOB
# =====================================================

@router.post(
    "/jobs",
    response_model=JobResponse
)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hr_admin
    )
):

    job = Job(

        title=payload.title,

        department=payload.department,

        location=payload.location,

        employment_type=payload.employment_type,

        hospital_name=payload.hospital_name,

        salary_range=payload.salary_range,

        experience_level=payload.experience_level,

        description=payload.description,

        requirements=payload.requirements,

        responsibilities=payload.responsibilities,

        deadline=payload.deadline
    )

    db.add(job)

    db.commit()

    db.refresh(job)

    return job
# =====================================================
# GET ALL JOBS
# PUBLIC
# =====================================================

@router.get(
    "/jobs",
    response_model=list[JobResponse]
)
def get_jobs(
    db: Session = Depends(get_db),

    status_filter: Optional[str] = Query(None),

    hospital_id: Optional[int] = Query(None),

    department: Optional[str] = Query(None)
):

    query = db.query(Job)

    if status_filter:

        query = query.filter(
            Job.status == status_filter
        )

    if hospital_id:

        query = query.filter(
            Job.hospital_id == hospital_id
        )

    if department:

        query = query.filter(
            Job.department.ilike(
                f"%{department}%"
            )
        )

    jobs = query.order_by(
        Job.id.desc()
    ).all()

    return jobs


# =====================================================
# GET SINGLE JOB
# =====================================================

@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse
)
def get_single_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


# =====================================================
# UPDATE JOB
# =====================================================

@router.put(
    "/jobs/{job_id}",
    response_model=JobResponse
)
def update_job(
    job_id: int,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hr_admin
    )
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    update_data = payload.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(job, key, value)

    db.commit()

    db.refresh(job)

    return job


# =====================================================
# DELETE JOB
# =====================================================

@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hr_admin
    )
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)

    db.commit()

    return {
        "message": "Job deleted successfully"
    }


# =====================================================
# APPLY FOR JOB
# PUBLIC
# =====================================================

@router.post(
    "/jobs/{job_id}/apply",
    response_model=JobApplicationResponse
)
def apply_for_job(
    job_id: int,
    payload: JobApplicationCreate,
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    application = JobApplication(

        full_name=payload.full_name,

        email=payload.email,

        phone=payload.phone,

        cv_url=payload.cv_url,

        address=payload.address,

        qualification=payload.qualification,

        years_of_experience=payload.years_of_experience,

        cover_letter=payload.cover_letter,

        job_id=job.id
    )

    db.add(application)

    db.commit()

    db.refresh(application)

    return application
# =====================================================
# GET APPLICATIONS
# DASHBOARD
# =====================================================

@router.get(
    "/applications",
    response_model=list[JobApplicationResponse]
)
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hr_admin
    )
):

    applications = db.query(
        JobApplication
    ).order_by(
        JobApplication.id.desc()
    ).all()

    return applications


# =====================================================
# UPDATE APPLICATION STATUS
# =====================================================

@router.put(
    "/applications/{application_id}/status"
)
def update_application_status(
    application_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_hr_admin
    )
):

    application = db.query(
        JobApplication
    ).filter(
        JobApplication.id == application_id
    ).first()

    if not application:

        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application.status = status_value

    db.commit()

    return {
        "message": "Application updated"
    }