# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Models and configuration for LM Studio backend.
"""

import os
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LMStudioConfig:
    """Configuration for LM Studio connection."""

    # Connection settings
    host: str = field(default_factory=lambda: os.environ.get("LMSTUDIO_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.environ.get("LMSTUDIO_PORT", "1234")))

    # Timeout settings
    timeout: float = 60.0
    connect_timeout: float = 10.0

    # Model settings
    default_model: str = ""  # Empty means use any loaded model
    auto_load: bool = True  # Auto-load model if not loaded

    # Prediction settings
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95

    # Caching
    cache_models: bool = True
    cache_ttl: float = 300.0  # 5 minutes

    @property
    def api_host(self) -> str:
        """Return host:port string."""
        return f"{self.host}:{self.port}"


@dataclass
class CachedModel:
    """Cached model reference with TTL."""

    model_id: str
    model_info: Any
    loaded_at: float
    last_used: float = field(default_factory=time.time)

    def is_expired(self, ttl: float) -> bool:
        """Check if cache entry is expired."""
        return time.time() - self.last_used > ttl

    def touch(self) -> None:
        """Update last used timestamp."""
        self.last_used = time.time()
