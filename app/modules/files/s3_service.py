from uuid import uuid4

from app.infrastructure.aws.clients.s3 import s3_client
from app.core.config import settings


class S3Service:

    def __init__(self):
        self.s3_client = s3_client
        self.bucket_name = settings.s3_bucket_name

    def generate_upload_url(
        self,
        user_id: str,
        content_type: str,
        expires_in: int = 300,
    ) -> dict:

        object_key = f"users/{user_id}/files/{uuid4()}"

        presigned_url = self.s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )

        return {
            "upload_url": presigned_url,
            "object_key": object_key,
            "expires_in": expires_in,
        }