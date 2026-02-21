#!/usr/bin/env python3
"""Resource core - minimal, parser-safe implementation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple
import time

try:
    from .base_core import BaseCore
except Exception:
    class BaseCore:  # pragma: no cover - fallback for tests
        def __init__(self, name: str = "Base", repo_root: Optional[str] = None) -> None:
            self.name = name


@dataclass
class QuotaConfig:
    max_tokens: Optional[int] = None
    max_time_seconds: Optional[int] = None
    max_cycles: Optional[int] = None


@dataclass
class ResourceUsage:
    tokens_input: int = 0
    tokens_output: int = 0
    start_time: float = field(default_factory=time.time)
    cycles: int = 0

    @property
    def total_tokens(self) -> int:
        return self.tokens_input + self.tokens_output

    @property
    def elapsed_time(self) -> float:
        return time.time() - self.start_time


class ResourceCore(BaseCore):
    """Simplified resource quota manager for tests."""

    def __init__(self, config: Optional[QuotaConfig] = None) -> None:
        super().__init__()
        self.config = config or QuotaConfig()
        self.usage = ResourceUsage()
        self._is_interrupted = False
        self._interrupt_reason: Optional[str] = None

    def update_usage(self, tokens_input: int = 0, tokens_output: int = 0, cycles: int = 0) -> bool:
        self.usage.tokens_input += tokens_input
        self.usage.tokens_output += tokens_output
        self.usage.cycles += cycles
        return True

    def check_quotas(self) -> Tuple[bool, Optional[str]]:
        if self.config.max_tokens and self.usage.total_tokens >= self.config.max_tokens:
            self._is_interrupted = True
            self._interrupt_reason = f"Token quota exceeded ({self.usage.total_tokens} >= {self.config.max_tokens})"
            return True, self._interrupt_reason

        if self.config.max_time_seconds and self.usage.elapsed_time >= self.config.max_time_seconds:
            self._is_interrupted = True
            self._interrupt_reason = (
                f"Time quota exceeded ({self.usage.elapsed_time:.2f}s >= {self.config.max_time_seconds}s)"
            )
            return True, self._interrupt_reason

        if self.config.max_cycles and self.usage.cycles >= self.config.max_cycles:
            self._is_interrupted = True
            self._interrupt_reason = f"Cycle quota exceeded ({self.usage.cycles} >= {self.config.max_cycles})"
            return True, self._interrupt_reason

        return False, None

    @property
    def is_interrupted(self) -> bool:
        return self._is_interrupted

    @property
    def interrupt_reason(self) -> Optional[str]:
        return self._interrupt_reason

    def get_report(self) -> Dict[str, Any]:
        return {
            "tokens_input": self.usage.tokens_input,
            "tokens_output": self.usage.tokens_output,
            "total_tokens": self.usage.total_tokens,
            "elapsed_time": self.usage.elapsed_time,
            "cycles": self.usage.cycles,
            "interrupted": self._is_interrupted,
            "reason": self._interrupt_reason,
        }

