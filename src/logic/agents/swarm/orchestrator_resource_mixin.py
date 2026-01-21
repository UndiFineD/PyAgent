#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import logging
from pathlib import Path
from typing import Any
from src.core.base.common.models import RateLimitConfig
from src.core.base.common.utils.file_lock_manager import FileLockManager
from src.core.base.logic.incremental_processor import IncrementalProcessor
from src.core.base.common.utils.rate_limiter import RateLimiter


class OrchestratorResourceMixin:
    """Resource management methods (rate limiting, locking, incremental processing) for OrchestratorAgent."""

    def enable_rate_limiting(self, config: RateLimitConfig | dict[str, Any] | None = None) -> None:
        """Enable rate limiting for API calls."""
        if isinstance(config, dict):
            config = RateLimitConfig(**config)

        self.rate_limiter = RateLimiter(config)
        logging.info(f"Rate limiting enabled: {config or 'default settings'}")

    def get_rate_limit_stats(self) -> dict[str, Any]:
        """Get current rate limiter statistics."""
        if hasattr(self, "rate_limiter"):
            return self.rate_limiter.get_stats()
        return {}

    def enable_file_locking(self, lock_timeout: float = 300.0) -> None:
        """Enable file locking."""
        self.lock_manager = FileLockManager(lock_timeout)
        logging.info(f"File locking enabled (timeout: {lock_timeout}s)")

    def enable_incremental_processing(self) -> None:
        """Enable incremental processing."""
        repo_root = getattr(self, "repo_root", Path("."))
        self.incremental_processor = IncrementalProcessor(repo_root)
        logging.info("Incremental processing enabled")

    def get_changed_files(self, files: list[Path]) -> list[Path]:
        """Get files that changed since last run."""
        if hasattr(self, "incremental_processor"):
            return self.incremental_processor.get_changed_files(files)
        return files

    def reset_incremental_state(self) -> None:
        """Reset incremental state."""
        if hasattr(self, "incremental_processor"):
            self.incremental_processor.reset_state()
