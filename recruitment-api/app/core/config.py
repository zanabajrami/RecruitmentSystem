from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    
    # Added to fix the AttributeError. If not provided in .env, it defaults to empty list
    BACKEND_CORS_ORIGINS: Optional[List[str]] = []

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()