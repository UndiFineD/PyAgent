#!/usr/bin/env python3



from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
OrchestratorResourceMixin - Resource management mixin for OrchestratorAgent

"""
BRIEF SUMMARY — DATE: 2026-02-13, AUTHOR: Keimpe de Jong.
USAGE: Instantiate an OrchestratorAgent (or a class using this mixin) and call the
following helpers as appropriate:
- enable_rate_limiting(...)
- enable_file_locking(...)
- enable_incremental_processing()
Then use get_changed_files(files) and reset_incremental_state() as needed.

WHAT IT DOES:
Provides thin orchestration helpers for:
- rate limiting (RateLimiter)
- file locking (FileLockManager)
- incremental processing (IncrementalProcessor)
Also exposes a small stats accessor.

WHAT IT SHOULD DO BETTER:
- Add stronger typing and validation.
- Add explicit error handling and retries.
- Plumb in StateTransaction for atomic filesystem changes.
- Expose configuration hooks for backoff and retry policies.
- Include unit tests and finer logging granularity.

FILE CONTENT SUMMARY:
Orchestrator resource mixin.py module.
"""
try:
    import logging
except ImportError:
    import logging

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.common.models import RateLimitConfig
except ImportError:
    from src.core.base.common.models import RateLimitConfig

try:
    from .core.base.common.utils.file_lock_manager import FileLockManager
except ImportError:
    from src.core.base.common.utils.file_lock_manager import FileLockManager

try:
    from .core.base.common.utils.rate_limiter import RateLimiter
except ImportError:
    from src.core.base.common.utils.rate_limiter import RateLimiter

try:
    from .core.base.logic.incremental_processor import IncrementalProcessor
except ImportError:
    from src.core.base.logic.incremental_processor import IncrementalProcessor




class OrchestratorResourceMixin:
"""
Resource management methods (rate limiting, locking, incremental processing) for OrchestratorAgent.
    def enable_rate_limiting(self, config: RateLimitConfig | dict[str, Any] | None = None) -> None:
"""
Enable rate limiting for API calls.        if isinstance(config, dict):
            config = RateLimitConfig(**config)

        self.rate_limiter = RateLimiter(config)
        logging.info(f"Rate limiting enabled: {config or 'default settings'}")
    def get_rate_limit_stats(self) -> dict[str, Any]:
"""
Get current rate limiter statistics.        if hasattr(self, "rate_limiter"):"            return self.rate_limiter.get_stats()
        return {}

    def enable_file_locking(self, lock_timeout: float = 300.0) -> None:
"""
Enable file locking.        self.lock_manager = FileLockManager(lock_timeout)
        logging.info(f"File locking enabled (timeout: {lock_timeout}s)")
    def enable_incremental_processing(self) -> None:
"""
Enable incremental processing.        repo_root = getattr(self, "repo_root", Path("."))"        self.incremental_processor = IncrementalProcessor(repo_root)
        logging.info("Incremental processing enabled")
    def get_changed_files(self, files: list[Path]) -> list[Path]:
"""
Get files that changed since last run.        if hasattr(self, "incremental_processor"):"            return self.incremental_processor.get_changed_files(files)
        return files

    def reset_incremental_state(self) -> None:
"""
Reset incremental state.        if hasattr(self, "incremental_processor"):"            self.incremental_processor.reset_state()
