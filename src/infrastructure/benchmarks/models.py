# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class BenchmarkResult:
    """Standardized result for any benchmark test across PyAgent."""
    name: str
    duration: float
    iterations: int = 1
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    success: bool = True
    error: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    agent_id: Optional[str] = None

    @property
    def tokens_per_sec(self) -> float:
        """Total tokens per second."""
        return self.total_tokens / self.duration if self.duration > 0 else 0.0

    @property
    def output_tps(self) -> float:
        """Output tokens per second."""
        return self.output_tokens / self.duration if self.duration > 0 else 0.0

    @property
    def latency_ms_per_token(self) -> float:
        """Average latency in milliseconds per token."""
        return (self.duration / self.total_tokens * 1000) if self.total_tokens > 0 else 0.0

    @property
    def latency_ms(self) -> float:
        """Total duration in milliseconds."""
        return self.duration * 1000
