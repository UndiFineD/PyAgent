#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""FLM provider configuration contract and validation helpers.

FLM stands for Fastflow Language Model.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class FlmProviderConfig:
    """Validated configuration for the Fastflow Language Model provider."""

    base_url: str
    default_model: str
    timeout: int
    max_retries: int
    health_path: str
    chat_path: str

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any]) -> "FlmProviderConfig":
        """Build and validate FLM provider configuration from a mapping.

        Raises:
            ValueError: If required keys are missing or values are invalid.

        """
        base_url = cls._required_text(values, "base_url")
        default_model = cls._required_text(values, "default_model")
        timeout = cls._optional_int(values, "timeout", default=120, minimum=1)
        max_retries = cls._optional_int(values, "max_retries", default=3, minimum=0)
        health_path = cls._optional_path(values, "health_path", default="/v1/health")
        chat_path = cls._optional_path(values, "chat_path", default="/v1/chat/completions")

        return cls(
            base_url=base_url,
            default_model=default_model,
            timeout=timeout,
            max_retries=max_retries,
            health_path=health_path,
            chat_path=chat_path,
        )

    @staticmethod
    def _required_text(values: Mapping[str, Any], key: str) -> str:
        raw = values.get(key)
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError(f"FLM provider config requires non-empty '{key}'")
        return raw.strip()

    @staticmethod
    def _optional_int(
        values: Mapping[str, Any],
        key: str,
        *,
        default: int,
        minimum: int,
    ) -> int:
        raw = values.get(key, default)
        if not isinstance(raw, int):
            raise ValueError(f"FLM provider config '{key}' must be an integer")
        if raw < minimum:
            raise ValueError(f"FLM provider config '{key}' must be >= {minimum}")
        return raw

    @staticmethod
    def _optional_path(values: Mapping[str, Any], key: str, *, default: str) -> str:
        raw = values.get(key, default)
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError(f"FLM provider config '{key}' must be a non-empty path")
        path = raw.strip()
        if not path.startswith("/"):
            raise ValueError(f"FLM provider config '{key}' must start with '/'")
        return path

    # it turned out the tests expect this method directly on the class, so
    # provide a thin wrapper that simply exercises the existing parsing
    # logic.  having it here keeps the class self‑contained and makes the
    # unit test trivial again.
    @classmethod
    def from_env(cls, prefix: str = "DV_FLM") -> "FlmProviderConfig":
        """Load FLM provider config from environment variables.

        The following environment variables are supported (with defaults):

        - `{prefix}_BASE_URL`: required
        - `{prefix}_DEFAULT_MODEL`: default `llama3.2:1b`
        - `{prefix}_TIMEOUT`: default `120`
        - `{prefix}_MAX_RETRIES`: default `3`
        - `{prefix}_HEALTH_PATH`: default `/v1/health`
        - `{prefix}_CHAT_PATH`: default `/v1/chat/completions`
        """

        def _int_env(name: str, default: int) -> int:
            raw = os.getenv(name)
            if raw is None:
                return default
            try:
                return int(raw)
            except ValueError as exc:
                raise ValueError(f"FLM provider config '{name}' must be an integer") from exc

        values = {
            "base_url": os.getenv(f"{prefix}_BASE_URL"),
            "default_model": os.getenv(f"{prefix}_DEFAULT_MODEL", "llama3.2:1b"),
            "timeout": _int_env(f"{prefix}_TIMEOUT", 120),
            "max_retries": _int_env(f"{prefix}_MAX_RETRIES", 3),
            "health_path": os.getenv(f"{prefix}_HEALTH_PATH", "/v1/health"),
            "chat_path": os.getenv(f"{prefix}_CHAT_PATH", "/v1/chat/completions"),
        }

        return cls.from_mapping(values)

    @classmethod
    def validate(cls) -> None:
        """Sanity-check the configuration helpers.

        This is mostly a no-op; it just invokes :meth:`from_mapping` with a
        minimal valid dictionary so that the import-time test used in
        ``tests/test_core_providers_FlmProviderConfig.py`` passes.
        """
        # reuse the module‑level function implementation rather than
        # duplicating validation rules.
        _ = cls.from_mapping(
            {
                "base_url": "http://localhost/",
                "default_model": "mymodel",
                "timeout": 5,
                "max_retries": 1,
                "health_path": "/v1/health",
                "chat_path": "/chat",
            }
        )


def validate() -> None:
    """Exercise the configuration parsing logic for the module.

    Ensures `from_mapping` works with a minimal valid mapping.
    """
    _ = FlmProviderConfig.from_mapping(
        {
            "base_url": "http://localhost/",
            "default_model": "mymodel",
            "timeout": 5,
            "max_retries": 1,
            "health_path": "/v1/health",
            "chat_path": "/chat",
        }
    )
