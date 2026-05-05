from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):+
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/generator_tz"
    REDIS_URL: str = "redis://redis:6379/0"
    
    SECRET_KEY: str = "change-this-secret"
    JWT_SECRET_KEY: str = "change-this-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "noreply@example.com"
    SMTP_PASSWORD: str = ""
    
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        extra = "ignore"
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


@lru_cache()
def get_settings() -> Settings:
    return Settings()