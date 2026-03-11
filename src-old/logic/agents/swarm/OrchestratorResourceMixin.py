#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/OrchestratorResourceMixin.description.md

# OrchestratorResourceMixin

**File**: `src\\logic\agents\\swarm\\OrchestratorResourceMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 52  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for OrchestratorResourceMixin.

## Classes (1)

### `OrchestratorResourceMixin`

Resource management methods (rate limiting, locking, incremental processing) for OrchestratorAgent.

**Methods** (6):
- `enable_rate_limiting(self, config)`
- `get_rate_limit_stats(self)`
- `enable_file_locking(self, lock_timeout)`
- `enable_incremental_processing(self)`
- `get_changed_files(self, files)`
- `reset_incremental_state(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.IncrementalProcessor.IncrementalProcessor`
- `src.core.base.models.RateLimitConfig`
- `src.core.base.utils.FileLockManager.FileLockManager`
- `src.core.base.utils.RateLimiter.RateLimiter`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/OrchestratorResourceMixin.improvements.md

# Improvements for OrchestratorResourceMixin

**File**: `src\\logic\agents\\swarm\\OrchestratorResourceMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 52 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `OrchestratorResourceMixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
import logging
from pathlib import Path
from typing import Any

from src.core.base.IncrementalProcessor import IncrementalProcessor
from src.core.base.models import RateLimitConfig
from src.core.base.utils.FileLockManager import FileLockManager
from src.core.base.utils.RateLimiter import RateLimiter


class OrchestratorResourceMixin:
    """Resource management methods (rate limiting, locking, incremental processing) for OrchestratorAgent."""

    def enable_rate_limiting(
        self, config: RateLimitConfig | dict[str, Any] | None = None
    ) -> None:
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
