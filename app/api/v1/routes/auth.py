from datetime import timedelta
import random
import string

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

from app.db.session import (
    get_db
)

from app.models.user import User

from app.schemas.user import (
    UserCreate
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.api.deps import (
    get_current_user
)

router = APIRouter()


# =====================================================
# VALID ROLES
# =====================================================

ALLOWED_ROLES = [

    "PATIENT",

    "DOCTOR",

    "HOSPITAL_ADMIN",

    "HR_ADMIN",

    "SUPER_ADMIN"
]


# =====================================================
# REGISTER USER / ADMIN
# =====================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db)
):

    # =========================================
    # CHECK EXISTING EMAIL
    # =========================================

    existing_user = db.query(User).filter(
        User.email == payload.email.lower()
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # =========================================
    # ROLE VALIDATION
    # =========================================

    role = (
        payload.role.upper()
        if payload.role
        else "PATIENT"
    )

    if role not in ALLOWED_ROLES:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    # =========================================
    # SECURITY:
    # ONLY FIRST SUPER ADMIN CAN SELF REGISTER
    # =========================================

    if role == "SUPER_ADMIN":

        existing_super_admin = db.query(
            User
        ).filter(
            User.role == "SUPER_ADMIN"
        ).first()

        if existing_super_admin:

            raise HTTPException(
                status_code=403,
                detail="Super admin already exists"
            )

    # =========================================
    # CREATE USER
    # =========================================

    new_user = User(

        full_name=payload.full_name.strip(),

        email=payload.email.lower().strip(),

        hashed_password=hash_password(
            payload.password
        ),

        role=role,

        hospital_id=payload.hospital_id
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    # =========================================
    # CREATE ACCESS TOKEN
    # =========================================

    token = create_access_token({

        "sub": new_user.email,

        "role": new_user.role,

        "user_id": new_user.id
    })

    return {

        "message":
            "User created successfully",

        "access_token":
            token,

        "token_type":
            "bearer",

        "user": {

            "id":
                new_user.id,

            "full_name":
                new_user.full_name,

            "email":
                new_user.email,

            "role":
                new_user.role,

            "hospital_id":
                new_user.hospital_id
        }
    }


# =====================================================
# LOGIN
# =====================================================

@router.post("/login")
def login(

    form_data:
    OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)
):

    # =========================================
    # FIND USER
    # =========================================

    user = db.query(User).filter(
        User.email == form_data.username.lower()
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # =========================================
    # VERIFY PASSWORD
    # =========================================

    if not verify_password(

        form_data.password,

        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # =========================================
    # CREATE TOKEN
    # =========================================

    token = create_access_token({

        "sub": user.email,

        "role": user.role,

        "user_id": user.id
    })

    return {

        "access_token":
            token,

        "token_type":
            "bearer",

        "user": {

            "id":
                user.id,

            "full_name":
                user.full_name,

            "email":
                user.email,

            "role":
                user.role,

            "hospital_id":
                user.hospital_id
        }
    }


# =====================================================
# CURRENT USER
# =====================================================

@router.get("/me")
def current_user(
    current_user: User = Depends(
        get_current_user
    )
):

    return {

        "id":
            current_user.id,

        "full_name":
            current_user.full_name,

        "email":
            current_user.email,

        "role":
            current_user.role,

        "hospital_id":
            current_user.hospital_id
    }


# =====================================================
# FORGOT PASSWORD
# =====================================================

@router.post("/forgot-password")
def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email.lower()
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # =========================================
    # GENERATE TEMP PASSWORD
    # =========================================

    temp_password = "".join(
        random.choices(
            string.ascii_letters + string.digits,
            k=8
        )
    )

    user.hashed_password = hash_password(
        temp_password
    )

    db.commit()

    return {

        "message":
            "Temporary password generated",

        "temporary_password":
            temp_password
    }


# =====================================================
# RESET PASSWORD
# =====================================================

@router.post("/reset-password")
def reset_password(

    old_password: str,

    new_password: str,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    # =========================================
    # VERIFY OLD PASSWORD
    # =========================================

    if not verify_password(

        old_password,

        current_user.hashed_password
    ):

        raise HTTPException(
            status_code=400,
            detail="Old password incorrect"
        )

    # =========================================
    # UPDATE PASSWORD
    # =========================================

    current_user.hashed_password = (
        hash_password(new_password)
    )

    db.commit()

    return {

        "message":
            "Password updated successfully"
    }