# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-X-AnyLabeling-Server\app\core\config.py
import os
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1


class LoggingConfig(BaseModel):
    level: str = "INFO"
    console_level: str = "INFO"
    file_enabled: bool = True
    file_path: Optional[str] = None
    rotation: str = "500 MB"
    retention: str = "30 days"
    format: str = "json"


class SecurityConfig(BaseModel):
    api_key_enabled: bool = False
    api_key: str = ""
    api_key_header: str = "Token"
    cors_origins: List[str] = ["*"]


class PerformanceConfig(BaseModel):
    request_timeout: int = 300
    max_image_size: int = 0
    rate_limit_enabled: bool = False
    rate_limit: str = "100/minute"


class ConcurrencyConfig(BaseModel):
    max_workers: int = 4
    max_queue_size: int = 50


class Settings(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    concurrency: ConcurrencyConfig = Field(default_factory=ConcurrencyConfig)

    @classmethod
    def load_from_yaml(cls, config_path: Path) -> "Settings":
        """Load configuration from YAML file.

        Args:
            config_path: Path to the configuration file.

        Returns:
            Settings instance with loaded configuration.
            User config values override defaults, but missing fields
            in user config will use defaults.
        """
        # Start with default settings
        default_settings = cls()
        default_dict = default_settings.model_dump()

        if not config_path.exists():
            return default_settings

        with open(config_path, "r") as f:
            user_data = yaml.safe_load(f) or {}

        # Deep merge: user config overrides defaults
        def deep_merge(default: dict, user: dict) -> dict:
            """Recursively merge user config into default config."""
            result = default.copy()
            for key, value in user.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        merged_data = deep_merge(default_dict, user_data)

        # Override API key from environment if not set in config
        if merged_data.get("security", {}).get("api_key") == "":
            env_key = os.getenv("XANYLABELING_API_KEY", "")
            if env_key:
                merged_data["security"]["api_key"] = env_key

        return cls(**merged_data)


def get_settings(config_path: Optional[Path] = None) -> tuple:
    """Get application settings.

    Args:
        config_path: Optional path to server.yaml config file.
                     If not provided, will check:
                     1. XANYLABELING_SERVER_CONFIG environment variable
                     2. Default configs/server.yaml

    Returns:
        Tuple of (Settings instance, actual config file path used).
    """
    if config_path is None:
        env_config = os.getenv("XANYLABELING_SERVER_CONFIG")
        if env_config:
            config_path = Path(env_config)
        else:
            config_path = Path(__file__).parent.parent.parent / "configs" / "server.yaml"
    else:
        config_path = Path(config_path)

    return Settings.load_from_yaml(config_path), config_path
