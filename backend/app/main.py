from fastapi import FastAPI
from app.api.v1.endpoints import perfis
from app.auth.fastapi_users import fastapi_users, auth_backend
from app.core.config import settings
from app.auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="nRadar API",
    description="API para o sistema de monitoramento de licitações nRadar.",
    version="0.1.0",
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(perfis.router, prefix="/api/v1/perfis", tags=["perfis"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do nRadar!"}
