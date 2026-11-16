import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


def get_request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.error_code,
            "message": exc.message,
            "request_id": get_request_id(request),
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:

    errors = []

    for error in exc.errors():
        location = error.get("loc", ())

        # Remove the "body" prefix from the field path
        field_path = ".".join(
            str(item) for item in location if item != "body"
        )

        errors.append({
            "field": field_path or "request",
            "message": error.get("msg", "Invalid value"),
            "type": error.get("type", "validation_error"),
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error_code": "VALIDATION_ERROR",
            "message": "Please correct the following fields.",
            "details": errors,
            "request_id": get_request_id(request),
        },
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    message = (
        exc.detail
        if isinstance(exc.detail, str)
        else "An HTTP error occurred"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": "HTTP_ERROR",
            "message": message,
            "request_id": get_request_id(request),
        },
        headers=exc.headers,
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled application exception",
        extra={"request_id": get_request_id(request)},
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "request_id": get_request_id(request),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unexpected_exception_handler,
    )