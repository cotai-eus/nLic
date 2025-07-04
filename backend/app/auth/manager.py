from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import UUID_ID

from app.auth.database import get_user_db
from app.core.config import settings
from app.models.user import User

class UserManager(UUIDIDMixin, BaseUserManager[User, UUID_ID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

from app.auth.database import get_async_session
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

async def get_user_manager():
    async for session in get_async_session():
        yield UserManager(SQLAlchemyUserDatabase(session, User))