from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.aws.cognito import get_user_details
from app.modules.auth.dependencies import (
    get_current_user,
    bearer_scheme,
)
from app.modules.users.service import UserService
from app.modules.users.models import User


async def get_authenticated_user(
    claims: dict = Depends(get_current_user),
    credentials=Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    user_details = get_user_details(credentials.credentials)

    user_service = UserService(db)

    return await user_service.get_or_create_user(
        cognito_sub=claims["sub"],
        email=user_details["email"],
    )