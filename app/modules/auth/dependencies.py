from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.modules.auth.service import AuthService
from app.infrastructure.aws.cognito import cognito_client
from app.modules.auth.token_service import verify_access_token
from app.core.exceptions import AuthenticationException


bearer_scheme = HTTPBearer(auto_error=False)


# Creates AuthService for login and password operations
def get_auth_service() -> AuthService:
    return AuthService(cognito=cognito_client)


# Authenticates users making protected API requests
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:

    if credentials is None:
        raise AuthenticationException(
            message="Authentication token is required.",
            error_code="MISSING_ACCESS_TOKEN",
        )

    return verify_access_token(credentials.credentials)