
import boto3

from app.core.config import settings


class CognitoClient:
    """
    Centralized AWS Cognito Identity Provider client.
    """

    def __init__(self) -> None:
        self.client = boto3.client(
            "cognito-idp",
            region_name=settings.aws_region,
        )

    @property
    def idp(self):
        return self.client


cognito = CognitoClient()
cognito_client = cognito.idp
