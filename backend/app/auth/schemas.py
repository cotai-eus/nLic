from fastapi_users import schemas
from fastapi_users_db_sqlalchemy import UUID_ID

class UserRead(schemas.BaseUser[UUID_ID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass
