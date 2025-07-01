from fastapi_users import FastAPIUsers
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, BearerTransport
from fastapi_users_db_sqlalchemy import UUID_ID

from app.auth.manager import get_user_manager
from app.core.config import settings
from app.models.user import User

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[
    User, UUID_ID
](
    get_user_manager,
    [auth_backend],
)