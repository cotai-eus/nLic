from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None
    SECRET_KEY: str = "supersecretkey"
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    SMTP_ENABLED: bool = False
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_SENDER_EMAIL: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
