"""
Configuration Management
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Anthropic
    anthropic_api_key: str

    # Stripe
    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_price_id_starter: str = "price_starter"
    stripe_price_id_standard: str = "price_standard"
    stripe_price_id_pro: str = "price_pro"

    # Clerk (Auth)
    clerk_secret_key: str
    clerk_publishable_key: str | None = None

    # Supabase
    supabase_url: str
    supabase_service_key: str

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
