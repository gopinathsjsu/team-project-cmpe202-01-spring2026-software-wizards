"""
Singleton Pattern — Settings is instantiated once via @lru_cache.
Any call to get_settings() returns the same instance.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://eventhub:eventhub_pass@localhost:5432/eventhub"

    # JWT
    SECRET_KEY: str = "change-me-to-a-random-256-bit-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # SMTP
    SMTP_HOST: str = "smtp.mailtrap.io"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@eventhub.dev"

    # Frontend URL (for password reset links)
    FRONTEND_URL: str = "http://localhost:5173"

    # AWS S3 (optional)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "eventhub-images"

    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()  # Singleton: called many times, instantiated once
def get_settings() -> Settings:
    return Settings()
