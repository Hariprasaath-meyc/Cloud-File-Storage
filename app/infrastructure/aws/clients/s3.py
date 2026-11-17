import boto3

from app.core.config import settings

session = boto3.Session(
  
    region_name=settings.aws_region,
)

s3_client = session.client("s3")