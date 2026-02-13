from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App Configuration
    app_name: str = "CS2 Trading Tracker"
    debug: bool = True
    
    # Steam API
    steam_api_key: str = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with your Steam API key
    steam_web_api_url: str = "https://api.steampowered.com"
    
    # Database
    database_url: str = "sqlite:///./cs2_tracker.db"
    
    # Security
    secret_key: str = "default_secret_key_change_in_production"
    
    # CSFloat
    csfloat_base_url: str = "https://csfloat.com"
    
    # Rate Limiting
    max_requests_per_minute: int = 60
    rate_limit_enabled: bool = True
    
    # Cache
    cache_enabled: bool = True
    cache_ttl: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Allow running without .env file
        extra = "ignore"


# Global settings instance
settings = Settings()
