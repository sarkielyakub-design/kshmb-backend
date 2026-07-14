from fastapi import (
    APIRouter,
    Depends,
    Request
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.audit import (
    AuditLog
)

from app.schemas.audit import (
    AuditLogResponse
)

from app.api.deps import (
    require_super_admin
)

from app.models.user import User

from app.services.audit_service import (
    create_audit_log
)

router = APIRouter()


# =========================
# CREATE TEST AUDIT LOG
# =========================

@router.post(
    "/test",
    response_model=AuditLogResponse
)
def test_audit_log(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_super_admin
    )
):

    ip_address = request.client.host

    log = create_audit_log(
        db=db,
        user_email=current_user.email,
        action="CREATE",
        module="AUDIT_SYSTEM",
        ip_address=ip_address,
        description="Test audit log created"
    )

    return log


# =========================
# GET AUDIT LOGS
# =========================

@router.get(
    "/",
    response_model=list[AuditLogResponse]
)
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_super_admin
    )
):

    logs = db.query(
        AuditLog
    ).order_by(
        AuditLog.created_at.desc()
    ).all()

    return logs