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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration and data structures regarding the model runner."""

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional


class RunnerState(Enum):
    """Model runner execution state."""

    IDLE = auto()  # Ready to accept work
    EXECUTING = auto()  # Currently running model forward
    WAITING = auto()  # Waiting regarding inputs
    CANCELLING = auto()  # Cancellation in progress
    SHUTDOWN = auto()  # Shutting down


@dataclass
class ModelInput:
    """Input regarding model execution."""

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
    """Output from scheduler regarding model runner."""

    request_ids: list[str] = field(default_factory=list)
    inputs: list[ModelInput] = field(default_factory=list)
    num_prefill: int = 0
    num_decode: int = 0
    total_tokens: int = 0
    block_tables: dict[str, list[int]] = field(default_factory=dict)
