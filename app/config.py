import os
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
from typing import List, Optional, Union, Any, Dict, Type, TypeVar
from functools import lru_cache

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "Synova AI API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT != "production"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./synova.db")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = os.getenv(
        "BACKEND_CORS_ORIGINS",
        "http://localhost:3000,http://localhost:8001"
    ).split(",")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
