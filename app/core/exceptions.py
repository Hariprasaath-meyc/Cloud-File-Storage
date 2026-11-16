

class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)


class AuthenticationException(AppException):
    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTHENTICATION_FAILED",
    ):
        super().__init__(message, 401, error_code)


class AuthorizationException(AppException):
    def __init__(
        self,
        message: str = "Permission denied",
        error_code: str = "FORBIDDEN",
    ):
        super().__init__(message, 403, error_code)


class ResourceNotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "RESOURCE_NOT_FOUND",
    ):
        super().__init__(message, 404, error_code)


class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource conflict",
        error_code: str = "RESOURCE_CONFLICT",
    ):
        super().__init__(message, 409, error_code)


class InvalidRequestException(AppException):
    def __init__(
        self,
        message: str = "Invalid request",
        error_code: str = "INVALID_REQUEST",
    ):
        super().__init__(message, 400, error_code)


class ExternalServiceException(AppException):
    def __init__(
        self,
        message: str = "External service unavailable",
        error_code: str = "EXTERNAL_SERVICE_ERROR",
    ):
        super().__init__(message, 503, error_code)

