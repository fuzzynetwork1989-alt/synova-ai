"""
Application configuration settings.

This module handles loading and validating configuration from environment variables.
"""
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    """Application settings.

    Loads settings from environment variables with sensible defaults.
    """
    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/synova_dev",
        description="PostgreSQL connection string"
    )
    TEST_DATABASE_URL: Optional[str] = Field(
        default=None,
        description="Test database connection string"
    )
    
    # Application settings
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    PROJECT_NAME: str = Field(
        default="Synova AI",
        description="Name of the project"
    )
    API_V1_STR: str = Field(
        default="/api/v1",
        description="API version 1 prefix"
    )

    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore',
        env_nested_delimiter='__'
    )

    @field_validator('DATABASE_URL', mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return str(PostgresDsn.build(
            scheme="postgresql",
            username="postgres",
            password="postgres",
            host="localhost",
            path="/synova_dev"
        ))

    @field_validator('TEST_DATABASE_URL', mode='before')
    @classmethod
    def assemble_test_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if v:
            return v
        # Default to in-memory SQLite for tests if not specified
        return "sqlite:///:memory:"


# Create settings instance
settings = Settings()
