
from app.modules.auth.service import AuthService
from app.infrastructure.aws.cognito import cognito_client


def get_auth_service() -> AuthService:
    return AuthService(cognito=cognito_client)
