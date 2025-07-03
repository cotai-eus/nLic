from dotenv import load_dotenv; load_dotenv()

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import perfis
from app.auth.fastapi_users import fastapi_users, auth_backend
from app.core.config import settings
from app.auth.schemas import UserRead, UserCreate

# Configure logging for fastapi_users
logging.getLogger("fastapi_users").setLevel(logging.DEBUG)

app = FastAPI(
    title="nRadar API",
    description="API para o sistema de monitoramento de licitações nRadar.",
    version="0.1.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(perfis.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do nRadar!"}
