import logging
from functools import wraps

from botocore.exceptions import BotoCoreError, ClientError

from app.core.exceptions import (
    AuthenticationException,
    ExternalServiceException,
    InvalidRequestException,
)

logger = logging.getLogger(__name__)


def handle_cognito_errors(operation: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except ClientError as exc:
                error_code = exc.response.get("Error", {}).get("Code")

                logger.warning(
                    "Cognito operation failed: operation=%s, code=%s",
                    operation,
                    error_code,
                )

                if error_code in {
                    "NotAuthorizedException",
                    "UserNotFoundException",
                }:
                        raise AuthenticationException(
                            message="Invalid email or password.",
                            error_code="INVALID_CREDENTIALS",
                        ) from exc

                if error_code in {
                    "InvalidPasswordException",
                    "InvalidParameterException",
                }:
                    raise InvalidRequestException(
                        message="Invalid authentication request.",
                        error_code="INVALID_AUTH_REQUEST",
                    ) from exc

                raise ExternalServiceException(
                    message="Authentication service is temporarily unavailable.",
                    error_code="COGNITO_SERVICE_UNAVAILABLE",
                ) from exc

            except BotoCoreError as exc:
                logger.exception(
                    "Cognito communication failed: operation=%s",
                    operation,
                )
                raise ExternalServiceException(
                    message="Authentication service is temporarily unavailable.",
                    error_code="COGNITO_SERVICE_UNAVAILABLE",
                ) from exc

        return wrapper
    return decorator