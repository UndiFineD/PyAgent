# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\big_3_super_agent.py\apps.py\content_gen.py\backend.py\src.py\content_gen_backend.py\config_bc0721c89a63.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\big-3-super-agent\apps\content-gen\backend\src\content_gen_backend\config.py

"""Configuration settings for the Content Generation Backend."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    openai_api_key: str

    video_storage_path: str = "./videos"

    max_poll_timeout: int = 600

    default_model: str = "sora-2"

    default_size: str = "1280x720"

    default_seconds: int = 4

    max_file_size: int = 10485760  # 10MB

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Global settings instance

settings = Settings()
