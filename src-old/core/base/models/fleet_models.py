#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/models/fleet_models.description.md

# fleet_models

**File**: `src\core\base\models\fleet_models.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 14 imports  
**Lines**: 84  
**Complexity**: 4 (simple)

## Overview

Models for fleet - wide state and resource management.

## Classes (5)

### `HealthCheckResult`

Result of agent health check.

### `IncrementalState`

State for incremental processing.

### `RateLimitConfig`

Configuration for rate limiting.

### `TokenBudget`

Manages token allocation.

**Methods** (4):
- `used(self)`
- `remaining(self)`
- `allocate(self, name, tokens)`
- `release(self, name)`

### `ShutdownState`

State for graceful shutdown.

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `base_models._empty_dict_str_any`
- `base_models._empty_dict_str_float`
- `base_models._empty_dict_str_int`
- `base_models._empty_dict_str_str`
- `base_models._empty_list_str`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enums.RateLimitStrategy`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/models/fleet_models.improvements.md

# Improvements for fleet_models

**File**: `src\core\base\models\fleet_models.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 84 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `fleet_models_test.py` with pytest tests

### Code Organization
- [TIP] **5 classes in one file** - Consider splitting into separate modules

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

"""Models for fleet - wide state and resource management."""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from .enums import RateLimitStrategy
from .base_models import (
    _empty_dict_str_any,
    _empty_dict_str_float,
    _empty_dict_str_str,
    _empty_list_str,
    _empty_dict_str_int,
)


@dataclass(slots=True)
class HealthCheckResult:
    """Result of agent health check."""

    healthy: bool
    backend_available: bool
    memory_ok: bool = True
    disk_ok: bool = True
    details: dict[str, Any] = field(default_factory=_empty_dict_str_any)


@dataclass(slots=True)
class IncrementalState:
    """State for incremental processing."""

    last_run_timestamp: float = 0.0
    processed_files: dict[str, float] = field(default_factory=_empty_dict_str_float)
    file_hashes: dict[str, str] = field(default_factory=_empty_dict_str_str)
    pending_files: list[str] = field(default_factory=_empty_list_str)


@dataclass(slots=True)
class RateLimitConfig:
    """Configuration for rate limiting."""

    requests_per_second: float = 10.0
    requests_per_minute: int = 60
    burst_size: int = 10
    strategy: RateLimitStrategy = RateLimitStrategy.TOKEN_BUCKET
    cooldown_seconds: float = 1.0


@dataclass(slots=True)
class TokenBudget:
    """Manages token allocation."""

    total: int
    allocations: dict[str, int] = field(default_factory=_empty_dict_str_int)

    @property
    def used(self) -> int:
        return sum(self.allocations.values())

    @property
    def remaining(self) -> int:
        return max(0, self.total - self.used)

    def allocate(self, name: str, tokens: int) -> None:
        capped = min(
            tokens,
            self.total - sum(v for k, v in self.allocations.items() if k != name),
        )
        self.allocations[name] = max(0, capped)

    def release(self, name: str) -> None:
        self.allocations.pop(name, None)


@dataclass(slots=True)
class ShutdownState:
    """State for graceful shutdown."""

    shutdown_requested: bool = False
    current_file: str | None = None
    completed_files: list[str] = field(default_factory=_empty_list_str)
    pending_files: list[str] = field(default_factory=_empty_list_str)
    start_time: float = field(default_factory=time.time)
