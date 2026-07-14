from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer
)

from fastapi.security.http import (
    HTTPAuthorizationCredentials
)

from jose import (
    JWTError,
    jwt
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import User

from app.core.config import settings


# =========================
# SECURITY
# =========================

security = HTTPBearer()


# =========================
# CURRENT USER
# =========================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication"
    )

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise credentials_exception

    return user


# =========================
# ACTIVE USER
# =========================

def get_current_active_user(
    current_user: User = Depends(
        get_current_user
    )
):

    if not current_user.is_active:

        raise HTTPException(
            status_code=403,
            detail="Inactive account"
        )

    return current_user


# =========================
# ROLE CHECKER
# =========================

def require_role(
    allowed_roles: list
):

    def role_checker(
        current_user: User = Depends(
            get_current_active_user
        )
    ):

        if current_user.role not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return role_checker


# =========================
# SUPER ADMIN
# =========================

def require_super_admin(
    current_user: User = Depends(
        get_current_active_user
    )
):

    if current_user.role != "SUPER_ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Super admin only"
        )

    return current_user


# =========================
# HR ADMIN
# =========================

def require_hr_admin(
    current_user: User = Depends(
        get_current_active_user
    )
):

    allowed_roles = [
        "SUPER_ADMIN",
        "HR_ADMIN"
    ]

    if current_user.role not in allowed_roles:

        raise HTTPException(
            status_code=403,
            detail="HR access required"
        )

    return current_user


# =========================
# HOSPITAL ADMIN
# =========================

def require_hospital_admin(
    current_user: User = Depends(
        get_current_active_user
    )
):

    allowed_roles = [
        "SUPER_ADMIN",
        "HOSPITAL_ADMIN"
    ]

    if current_user.role not in allowed_roles:

        raise HTTPException(
            status_code=403,
            detail="Hospital admin access required"
        )

    return current_user


# =========================
# DOCTOR ACCESS
# =========================

def require_doctor(
    current_user: User = Depends(
        get_current_active_user
    )
):

    allowed_roles = [
        "SUPER_ADMIN",
        "DOCTOR"
    ]

    if current_user.role not in allowed_roles:

        raise HTTPException(
            status_code=403,
            detail="Doctor access required"
        )

    return current_user