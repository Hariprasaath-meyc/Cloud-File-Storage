
from app.core.exceptions import (
    ConflictException,
    InvalidRequestException,
    ExternalServiceException,
)


class EmailAlreadyRegistered(ConflictException):
    def __init__(self):
        super().__init__(
            message="An account with this email already exists.",
            error_code="EMAIL_ALREADY_REGISTERED",
        )


class InvalidSignupRequest(InvalidRequestException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="INVALID_SIGNUP_REQUEST",
        )


class CognitoServiceError(ExternalServiceException):
    def __init__(self):
        super().__init__(
            message="Authentication service is temporarily unavailable.",
            error_code="COGNITO_SERVICE_UNAVAILABLE",
        )
