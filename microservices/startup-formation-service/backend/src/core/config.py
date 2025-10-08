"""
Configuration settings for Startup Formation Service
"""

import os
from typing import List, Optional
from pydantic import BaseModel, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]

    # Trusted hosts for security
    TRUSTED_HOSTS: Optional[List[str]] = None

    # Database Settings
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/startup_formation"

    # Redis Settings (for caching and sessions)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Message Queue Settings
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"

    # External API Keys and Credentials
    WA_SOS_API_KEY: Optional[str] = None
    WA_DOR_API_KEY: Optional[str] = None
    IRS_API_CREDENTIALS: Optional[str] = None

    # Document Generation Settings
    DOCUMENTS_DIR: str = "/tmp/documents"
    DOCUMENT_TEMPLATES_DIR: str = "templates/documents"

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Monitoring Settings
    SENTRY_DSN: Optional[str] = None
    OTEL_ENDPOINT: Optional[str] = None

    # Service Dependencies
    LEGAL_COMPLIANCE_SERVICE_URL: str = "http://localhost:8001"
    BUSINESS_FORMATION_SERVICE_URL: str = "http://localhost:8002"
    CONTENT_STRATEGY_SERVICE_URL: str = "http://localhost:8003"

    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not (v.startswith(("postgresql://", "postgresql+asyncpg://", "sqlite://", "sqlite+aiosqlite://"))):
            raise ValueError("DATABASE_URL must be a valid PostgreSQL or SQLite URL")
        return v

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Environment-specific configurations
def get_settings() -> Settings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development")

    if env == "production":
        # Production settings would override defaults
        pass
    elif env == "testing":
        # Test settings
        settings.DEBUG = True
        settings.DATABASE_URL = "sqlite+aiosqlite:///./test.db"

    return settings
