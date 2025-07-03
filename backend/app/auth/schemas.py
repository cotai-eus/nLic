from fastapi_users import schemas
from fastapi_users_db_sqlalchemy import UUID_ID

class UserRead(schemas.BaseUser[UUID_ID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    email: str

class UserUpdate(schemas.BaseUserUpdate):
    pass
