import asyncio

from sqlalchemy import text
from app.infrastructure.database.session import engine


async def check_database():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print("Query result:", result.scalar())

    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check_database())