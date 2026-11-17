from app.core.config import settings
from app.infrastructure.aws.clients.s3 import s3_client


def check_s3_connection():
    s3_client.head_bucket(
        Bucket=settings.s3_bucket_name
    )
    print("S3 connection successful!")


if __name__ == "__main__":
    check_s3_connection()