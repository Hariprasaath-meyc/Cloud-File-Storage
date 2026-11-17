from app.modules.files.s3_service import S3Service


class FileService:

    def __init__(self, s3_service: S3Service):
        self.s3_service = s3_service

    def generate_upload_url(
        self,
        user_id: str,
        filename: str,
        content_type: str,
    ) -> dict:

        result = self.s3_service.generate_upload_url(
            user_id=user_id,
            content_type=content_type,
        )

        return {
            "message": "Upload URL generated successfully",
            **result,
        }