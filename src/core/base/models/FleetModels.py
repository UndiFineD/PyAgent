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

"""Models for fleet - wide state and resource management."""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any
from .CoreEnums import RateLimitStrategy
from .BaseModels import (
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
