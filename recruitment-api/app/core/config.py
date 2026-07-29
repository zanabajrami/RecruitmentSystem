from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application Metadata
    PROJECT_NAME: str = "Recruitment API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration
    # Allows requests from specified origins or fallback to local origins
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Database Connection
    # Fallback to local SQLite database if not configured in .env
    DATABASE_URL: str = "sqlite:///./recruitment.db"
    
    # Redis Configuration
    # Used for Celery asynchronous background tasks
    REDIS_URL: str = "redis://localhost:6379/0"

    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # Ignores unknown environment variables in .env without raising validation errors
        extra="ignore"
    )

settings = Settings()