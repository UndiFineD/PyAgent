# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration and enums for advanced request scheduling."""

from dataclasses import dataclass
from enum import Enum, auto


class RequestPriority(Enum):
    """Priority levels for inference requests."""
    CRITICAL = 0    # System-critical (must execute immediately)
    HIGH = 1        # User-facing, latency-sensitive
    NORMAL = 2      # Standard priority
    LOW = 3         # Background processing
    BACKGROUND = 4  # Batch jobs, can be heavily preempted


class RequestState(Enum):
    """State of an inference request."""
    WAITING = auto()           # In queue, not yet scheduled
    RUNNING = auto()           # Currently executing
    PREEMPTED = auto()         # Paused to make room for higher priority
    WAITING_KV_CACHE = auto()  # Waiting for remote KV cache
    COMPLETED = auto()         # Finished successfully
    ABORTED = auto()           # Cancelled by user
    FAILED = auto()            # Error during execution


class PreemptionReason(Enum):
    """Reason for request preemption."""
    HIGHER_PRIORITY = auto()   # Higher priority request arrived
    MEMORY_PRESSURE = auto()   # Need to free GPU memory
    TIMEOUT = auto()           # Exceeded time limit
    TOKEN_BUDGET = auto()      # Token budget exhausted
    DEADLINE = auto()          # Deadline approaching for other requests


@dataclass
class SchedulerConfig:
    """Configuration for the request scheduler."""
    max_running_requests: int = 32
    max_tokens_per_batch: int = 4096
    max_prompt_tokens: int = 2048
    preemption_enabled: bool = True
    preemption_mode: str = "swap"  # "swap" or "recompute"
    chunked_prefill_enabled: bool = True
    chunk_token_threshold: int = 512
    starvation_prevention: bool = True
    deadline_scheduling: bool = True
