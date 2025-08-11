# app/config.py
from pydantic import BaseSettings, EmailStr, AnyUrl


class Settings(BaseSettings):
    APP_NAME: str = "fastapi-celery-mail"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    ALGORITHM: str = "HS256"

    # Database
    DATABASE_URL: str = "sqlite:///./test.db"  # override in production (e.g. postgres URL)

    # Celery / Redis
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"

    # SMTP
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: EmailStr = "noreply@example.com"
    SMTP_USE_TLS: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
