from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.infrastructure.database.session import get_db
from app.modules.users.dependencies import get_authenticated_user
from app.modules.users.models import User

from app.modules.files.schemas import (
    UpdateFileVersionRequest,
    UploadURLRequest,
    UploadURLResponse,
)
from app.modules.files.service import FileService
from app.modules.files.s3_service import S3Service


router = APIRouter(prefix="/files", tags=["Files"])


def get_file_service(
    db: AsyncSession = Depends(get_db),
) -> FileService:
    return FileService(
        db=db,
        s3_service=S3Service(),
    )


@router.post(
    "/upload-url",
    response_model=UploadURLResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_upload_url(
    payload: UploadURLRequest,
    current_user: User = Depends(get_authenticated_user),
    idempotency_key: UUID = Header(alias="Idempotency-Key"),
    file_service: FileService = Depends(get_file_service),
):
    return await file_service.generate_upload_url(
        user_id=current_user.id,
        filename=payload.filename,
        content_type=payload.content_type,
        idempotency_key=idempotency_key,  # Added
    )


@router.post("/{file_id}/versions/upload-url")
async def create_file_version_upload_url(
    file_id: UUID,
    payload: UpdateFileVersionRequest,
    current_user: User = Depends(get_authenticated_user),
    file_service: FileService = Depends(get_file_service),
):
    return await file_service.generate_version_upload_url(
        file_id=file_id,
        user_id=current_user.id,
        payload=payload,
    )