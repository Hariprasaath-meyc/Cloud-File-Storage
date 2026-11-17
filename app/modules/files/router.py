from fastapi import APIRouter, Depends, status

from app.modules.auth.dependencies import get_current_user
from app.modules.files.schemas import (
    UploadURLRequest,
    UploadURLResponse,
)
from app.modules.files.service import FileService
from app.modules.files.s3_service import S3Service


router = APIRouter(prefix="/files", tags=["Files"])


def get_file_service() -> FileService:
    s3_service = S3Service()
    return FileService(s3_service=s3_service)


@router.post(
    "/upload-url",
    response_model=UploadURLResponse,
    status_code=status.HTTP_200_OK,
)
def generate_upload_url(
    payload: UploadURLRequest,
    current_user: dict = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
):
    return file_service.generate_upload_url(
        user_id=current_user["sub"],
        filename=payload.filename,
        content_type=payload.content_type,
    )

