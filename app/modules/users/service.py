from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.repository import UserRepository
from app.modules.users.models import User


class UserService:

    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
        self.db = db

    async def get_or_create_user(
        self,
        cognito_sub: str,
        email: str,
    ) -> User:

        user = await self.repository.get_by_cognito_sub(cognito_sub)

        if user:
            return user

        user = await self.repository.create(
            cognito_sub=cognito_sub,
            email=email,
        )

        await self.db.commit()
        await self.db.refresh(user)

        return user