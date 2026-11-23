
from uuid import uuid4, UUID
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


from app.modules.files.models.models import FileStatus
from app.modules.files.repository import FileRepository
from app.modules.files.s3_service import S3Service
from app.modules.files.schemas import UpdateFileVersionRequest


class FileService:

    def __init__(
        self,
        db: AsyncSession,
        s3_service: S3Service,
    ):
        self.db = db
        self.file_repository = FileRepository(db)
        self.s3_service = s3_service

    async def generate_upload_url(
        self,
        user_id: UUID,
        filename: str,
        content_type: str,
        idempotency_key: UUID,
    ) -> dict:

        try:
            # 1. Check whether this request was already received.
            existing_file = (
                await self.file_repository.get_by_idempotency_key(
                    idempotency_key=idempotency_key
                )
            )

            if existing_file:
                return await self._handle_existing_upload(
                    file=existing_file,
                    user_id=user_id,
                    filename=filename,
                    content_type=content_type,
                )

            # 2. Generate a new logical file ID.
            file_id = uuid4()

            # 3. Set upload intent expiry.
            upload_expires_at = (
                datetime.now(timezone.utc) + timedelta(minutes=30)
            )

            # 4. Generate presigned URL.
            upload_details = self.s3_service.generate_upload_url(
                user_id=str(user_id),
                file_id=str(file_id),
                content_type=content_type,
                expires_in=500,
            )

            # 5. Create file record.
            file = await self.file_repository.create(
                file_id=file_id,
                user_id=user_id,
                original_filename=filename,
                bucket_name=upload_details["bucket_name"],
                object_key=upload_details["object_key"],
                content_type=content_type,
                idempotency_key=idempotency_key,
                upload_expires_at=upload_expires_at,
            )

            await self.db.commit()

            # 6. Return upload details.
            return {
                "file_id": str(file.id),
                "filename": file.original_filename,
                "status": file.status.value,
                "upload_url": upload_details["upload_url"],
                "object_key": file.object_key,
                "expires_in": upload_details["expires_in"],
            }

        except IntegrityError:
            # Another concurrent request may have inserted this key.
            await self.db.rollback()

            existing_file = (
                await self.file_repository.get_by_idempotency_key(
                    idempotency_key=idempotency_key
                )
            )

            if existing_file is None:
                raise

            return await self._handle_existing_upload(
                file=existing_file,
                user_id=user_id,
                filename=filename,
                content_type=content_type,
            )

        except Exception:
            await self.db.rollback()
            raise

    async def generate_version_upload_url(
        self,
        file_id: UUID,
        user_id: UUID,
        payload: UpdateFileVersionRequest,
    ) -> dict:

        # 1. Retrieve existing logical file
        file = await self.file_repository.get_by_id_and_user_id(
            file_id=file_id,
            user_id=user_id,
        )

        if file is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this file",
            )

        # 2. Verify file status
        if file.status.value != "ACTIVE":
            raise ValueError("File is not available for updating")

        # 3. Reuse existing S3 object location
        upload_details = self.s3_service.generate_version_upload_url(
            bucket_name=file.bucket_name,
            object_key=file.object_key,
            content_type=payload.content_type,
            expires_in=500,
        )

        # 4. Return upload details
        return {
            "file_id": str(file.id),
            "filename": file.original_filename,
            "status": file.status.value,
            "upload_url": upload_details["upload_url"],
            "object_key": file.object_key,
            "expires_in": upload_details["expires_in"],
        }

    async def _handle_existing_upload(
        self,
        file,
        user_id: UUID,
        filename: str,
        content_type: str,
    ) -> dict:

        # 1. Verify ownership.
        if file.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Idempotency key already exists",
            )

        # 2. Ensure the key is not reused for a different request.
        if (
            file.original_filename != filename
            or file.content_type != content_type
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Idempotency key was already used with different upload details",
            )

        # 3. Check file status.
        if file.status == FileStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Upload already completed. Use the version upload endpoint to replace this file.",
            )

        if file.status == FileStatus.PROCESSING:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="File upload is currently being processed",
            )

        if file.status != FileStatus.UPLOADING:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"File cannot be uploaded in its current status: {file.status.value}",
            )

        # 4. Reuse the existing file ID and generate a fresh URL.
        upload_details = self.s3_service.generate_upload_url(
            user_id=str(user_id),
            file_id=str(file.id),
            content_type=content_type,
            expires_in=300,
        )

        # 5. Ensure the generated key matches the existing logical file.
        if upload_details["object_key"] != file.object_key:
            raise RuntimeError("Generated S3 object key does not match existing file")

        return {
            "file_id": str(file.id),
            "filename": file.original_filename,
            "status": file.status.value,
            "upload_url": upload_details["upload_url"],
            "object_key": file.object_key,
            "expires_in": upload_details["expires_in"],
        }