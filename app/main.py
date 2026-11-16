from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.modules.auth.router import router as auth_router
from app.core.exceptions import (
    AuthenticationException,
    ResourceNotFoundException,
)


app =FastAPI(
    title="Cloud File Storage",
    version="1.0.0"
)

register_exception_handlers(app)

app.include_router(auth_router)

@app.get("/health")
async def health_check():
    return{
        "status":"healthy",
        "application":"Cloudfile Storage"
    }


@app.get("/test-auth-error")
async def test_auth_error():
    raise AuthenticationException(
        message="Invalid email or password"
    )


@app.get("/test-not-found")
async def test_not_found():
    raise ResourceNotFoundException(
        message="File not found"
    )

