
from uuid import UUID
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.files.models.models import File, FileStatus



class FileRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        file_id: UUID,
        user_id: UUID,
        original_filename: str,
        bucket_name: str,
        object_key: str,
        content_type: str,
        upload_expires_at: datetime,
    ) -> File:

        file = File(
            id=file_id,
            user_id=user_id,
            original_filename=original_filename,
            bucket_name=bucket_name,
            object_key=object_key,
            content_type=content_type,
            upload_expires_at=upload_expires_at,
            status=FileStatus.UPLOADING,
        )

        self.db.add(file)

        await self.db.flush()

        return file

    async def get_by_id(self, file_id: UUID) -> File | None:

        result = await self.db.execute(
            select(File).where(File.id == file_id)
        )

        return result.scalar_one_or_none()
