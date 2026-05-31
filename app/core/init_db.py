from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.core.db import AsyncSessionLocal
from app.core.user import UserManager
from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(
    email: str,
    password: str,
    is_superuser: bool = False,
) -> None:
    async with AsyncSessionLocal() as session:
        user_db = SQLAlchemyUserDatabase(session, User)
        user_manager = UserManager(user_db)

        try:
            await user_manager.create(
                UserCreate(
                    email=email,
                    password=password,
                    is_superuser=is_superuser,
                )
            )
        except UserAlreadyExists:
            return
