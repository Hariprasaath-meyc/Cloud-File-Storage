
from uuid import uuid4, UUID
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession


from app.modules.files.repository import FileRepository
from app.modules.files.s3_service import S3Service


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
    ) -> dict:

        try:
            # 1. Generate a single logical file ID.
            file_id = uuid4()

            # 2. Application-level upload intent expiry.
            upload_expires_at = (
                datetime.now(timezone.utc) + timedelta(minutes=30)
            )

            # 3. Generate presigned URL using the same file ID.
            upload_details = self.s3_service.generate_upload_url(
                user_id=str(user_id),
                file_id=str(file_id),
                content_type=content_type,
                expires_in=300,
            )

            # 4. Create upload intent in PostgreSQL.
            file = await self.file_repository.create(
                file_id=file_id,
                user_id=user_id,
                original_filename=filename,
                bucket_name=upload_details["bucket_name"],
                object_key=upload_details["object_key"],
                content_type=content_type,
                upload_expires_at=upload_expires_at,
            )

            # 5. Commit the transaction.
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

        except Exception:
            await self.db.rollback()
            raise
