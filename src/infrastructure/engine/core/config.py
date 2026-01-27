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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration and data structures for the inference engine core."""

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set


class RequestStatus(Enum):
    """Status of a request in the engine."""

    WAITING = auto()
    RUNNING = auto()
    FINISHED = auto()
    ABORTED = auto()
    PREEMPTED = auto()
    WAITING_FOR_REMOTE = auto()


class FinishReason(Enum):
    """Reason why a request finished."""

    STOP = auto()
    LENGTH = auto()
    ABORT = auto()
    ERROR = auto()
    EOS = auto()


@dataclass
class Request:  # pylint: disable=too-many-instance-attributes
    """A request to be processed by the engine."""

    request_id: str
    prompt_token_ids: List[int]
    sampling_params: Optional[Dict[str, Any]] = None
    arrival_time: float = field(default_factory=time.time)
    status: RequestStatus = RequestStatus.WAITING
    num_tokens: int = 0
    num_computed_tokens: int = 0
    output_token_ids: List[int] = field(default_factory=list)
    finish_reason: Optional[FinishReason] = None
    client_index: int = 0
    lora_request: Optional[Any] = None
    cache_salt: Optional[str] = None
    trace_headers: Optional[Dict[str, str]] = None

    def __post_init__(self) -> None:
        self.num_tokens = len(self.prompt_token_ids)

    def get_finished_reason(self) -> Optional[FinishReason]:
        """Get the reason why this request finished."""
        return self.finish_reason

    def is_finished(self) -> bool:
        """Check if request is finished."""
        return self.status in (RequestStatus.FINISHED, RequestStatus.ABORTED)


@dataclass
class SchedulerOutput:
    """Output from the scheduler containing batch info."""

    scheduled_requests: List[Request] = field(default_factory=list)
    num_scheduled_tokens: Dict[str, int] = field(default_factory=dict)
    total_num_scheduled_tokens: int = 0
    num_prefill_tokens: int = 0
    num_decode_tokens: int = 0
    preempted_requests: List[Request] = field(default_factory=list)

    def is_empty(self) -> bool:
        """Check if no requests were scheduled."""
        return self.total_num_scheduled_tokens == 0


@dataclass
class ModelRunnerOutput:
    """Output from the model runner."""

    req_ids: List[str] = field(default_factory=list)
    req_id_to_index: Dict[str, int] = field(default_factory=dict)
    sampled_token_ids: List[List[int]] = field(default_factory=list)
    logprobs: Optional[List[Any]] = None
    prompt_logprobs_dict: Dict[str, Any] = field(default_factory=dict)
    pooler_output: List[Any] = field(default_factory=list)

    @classmethod
    def empty(cls) -> "ModelRunnerOutput":
        """Create an empty output."""
        return cls()


@dataclass
class EngineCoreOutput:
    """Output for a single request."""

    request_id: str
    new_token_ids: List[int] = field(default_factory=list)
    finish_reason: Optional[FinishReason] = None
    new_logprobs: Optional[List[Any]] = None
    pooling_output: Optional[Any] = None
    stop_reason: Optional[str] = None


@dataclass
class EngineCoreOutputs:
    """Batch of outputs from the engine core."""

    outputs: List[EngineCoreOutput] = field(default_factory=list)
    scheduler_stats: Optional[Dict[str, Any]] = None
    timestamp: float = field(default_factory=time.time)
    finished_requests: Optional[Set[str]] = None
