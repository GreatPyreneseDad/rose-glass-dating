"""
Configuration Management
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Anthropic
    anthropic_api_key: str

    # Stripe (Optional for MVP)
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    stripe_price_id_starter: str = "price_starter"
    stripe_price_id_standard: str = "price_standard"
    stripe_price_id_pro: str = "price_pro"

    # Clerk (Auth) - Optional for MVP, uses dev mode
    clerk_secret_key: Optional[str] = None
    clerk_publishable_key: Optional[str] = None

    # Supabase (Optional for MVP, can run without DB)
    supabase_url: Optional[str] = None
    supabase_service_key: Optional[str] = None

    # App
    app_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    environment: str = "development"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
