from pydantic import BaseModel, Field


class UploadURLRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(min_length=1)


class UploadURLResponse(BaseModel):
    message: str
    upload_url: str
    object_key: str
    expires_in: int