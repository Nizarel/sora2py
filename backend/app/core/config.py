"""
Configuration settings for the Video Studio API
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Coca-Cola Sora-2 Video Studio"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Azure OpenAI (Sora-2)
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_DEPLOYMENT: str = "sora-2"
    
    # Azure Storage
    AZURE_STORAGE_CONNECTION_STRING: str
    AZURE_STORAGE_CONTAINER_NAME: str = "videos"
    
    # Database
    DATABASE_URL: str
    
    # Redis (for Celery)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Video Settings
    MAX_VIDEO_DURATION: int = 120  # seconds
    DEFAULT_VIDEO_RESOLUTION: str = "1280x720"
    MAX_RESOLUTION: str = "1920x1080"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
