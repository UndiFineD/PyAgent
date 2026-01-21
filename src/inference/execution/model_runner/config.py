# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration and data structures for the model runner."""

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class RunnerState(Enum):
    """Model runner execution state."""
    IDLE = auto()        # Ready to accept work
    EXECUTING = auto()   # Currently running model forward
    WAITING = auto()     # Waiting for inputs
    CANCELLING = auto()  # Cancellation in progress
    SHUTDOWN = auto()    # Shutting down


@dataclass
class ModelInput:
    """Input for model execution."""
    request_id: str
    input_ids: list[int] = field(default_factory=list)
    attention_mask: list[int] = field(default_factory=list)
    position_ids: list[int] = field(default_factory=list)
    block_tables: list[list[int]] = field(default_factory=list)
    context_lens: list[int] = field(default_factory=list)
    num_prefill_tokens: int = 0
    num_decode_tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelOutput:
    """Output from model execution."""
    request_id: str
    output_ids: list[int] = field(default_factory=list)
    logprobs: Optional[list[float]] = None
    hidden_states: Optional[list[float]] = None
    finished: bool = False
    error: Optional[str] = None
    latency_ms: float = 0.0
    tokens_generated: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass
class SchedulerOutput:
    """Output from scheduler for model runner."""
    request_ids: list[str] = field(default_factory=list)
    inputs: list[ModelInput] = field(default_factory=list)
    num_prefill: int = 0
    num_decode: int = 0
    total_tokens: int = 0
    block_tables: dict[str, list[int]] = field(default_factory=dict)
