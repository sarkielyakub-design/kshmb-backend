from sqlalchemy.orm import Session

from app.models.audit import AuditLog


def create_audit_log(
    db: Session,
    user_email: str,
    action: str,
    module: str,
    ip_address: str,
    description: str
):

    log = AuditLog(
        user_email=user_email,
        action=action,
        module=module,
        ip_address=ip_address,
        description=description
    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log