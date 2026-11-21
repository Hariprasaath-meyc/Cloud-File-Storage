from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_cognito_sub(self, cognito_sub: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.cognito_sub == cognito_sub)
        )
        return result.scalar_one_or_none()

    async def create(self, cognito_sub: str, email: str) -> User:
        user = User(
            cognito_sub=cognito_sub,
            email=email,
        )

        self.db.add(user)
        await self.db.flush()

        return user