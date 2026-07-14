from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from app.services.upload_service import (
    upload_file
)

from app.api.deps import (
    get_current_active_user
)

from app.models.user import User

router = APIRouter()


@router.post("/")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(
        get_current_active_user
    )
):

    file_url = upload_file(file)

    return {
        "message": "File uploaded successfully",
        "url": file_url
    }