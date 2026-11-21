
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

def get_user_details(access_token: str) -> dict:
    response = cognito_client.get_user(
        AccessToken=access_token
    )

    attributes = {
        item["Name"]: item["Value"]
        for item in response["UserAttributes"]
    }

    return {
        "sub": attributes["sub"],
        "email": attributes["email"],
    }