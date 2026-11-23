from uuid import UUID

from pydantic import BaseModel, Field


class UploadURLRequest(BaseModel):
    filename: str = Field(
        min_length=1,
        max_length=255,
    )

    content_type: str = Field(
        min_length=1,
        max_length=100,
    )


class UploadURLResponse(BaseModel):
    file_id: UUID
    filename: str
    status: str
    upload_url: str
    object_key: str
    expires_in: int

class UpdateFileVersionRequest(BaseModel):
    filename: str = Field(min_length=1)
    content_type: str