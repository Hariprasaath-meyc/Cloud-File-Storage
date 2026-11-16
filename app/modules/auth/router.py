from fastapi import APIRouter, Depends

from app.modules.auth.schemas import LoginRequest, LoginResponse, PasswordChangeRequest
from app.modules.auth.service import AuthService
from app.modules.auth.dependencies import get_auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.login(payload)


@router.post("/complete-password-change", response_model=LoginResponse)
def complete_password_change(
    payload: PasswordChangeRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.complete_password_change(payload)