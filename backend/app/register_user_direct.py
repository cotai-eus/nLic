import asyncio
from app.auth.manager import UserManager
from app.auth.schemas import UserCreate
from app.db.session import async_session_maker
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from app.models.user import User

async def register_user_directly():
    async with async_session_maker() as session:
        user_db = SQLAlchemyUserDatabase(session, User)
        user_manager = UserManager(user_db)
        user_create = UserCreate(email="direct_test@example.com", password="direct_password")
        try:
            user = await user_manager.create(user_create, safe=True)
            print(f"User registered directly: {user.email}")
        except Exception as e:
            print(f"Direct user registration failed: {e}")

if __name__ == "__main__":
    asyncio.run(register_user_directly())