import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./zentrasec.db"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    llm_api_key: str = ""
    llm_api_url: str = ""
    threat_intel_api_key: str = ""
    threat_intel_provider: str = "demo"
    response_provider: str = "simulated"
    ml_enabled: bool = True
    seed_demo_data: bool = True
    default_analyst_username: str = "analyst"
    default_analyst_password: str = "analyst123"
    google_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
