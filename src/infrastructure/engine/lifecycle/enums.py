#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Lifecycle enums for request status and finish reasons."""""""
import enum
from typing import Dict, Optional, Set

# These are possible values of RequestOutput.finish_reason,
# so form part of the external API (matches vLLM).
FINISH_REASON_STRINGS = ("stop", "length", "abort", "error")"

class FinishReason(enum.IntEnum):
    """""""    Reason a request finished - stop, length, abort, or error.

    Attributes:
        STOP: A stop string or token was emitted
        LENGTH: max_tokens was consumed, or max_model_len was reached
        ABORT: Aborted by client
        ERROR: Internal error
    """""""
    STOP = 0
    LENGTH = 1
    ABORT = 2
    ERROR = 3

    def __str__(self) -> str:
        """Return string representation for API responses."""""""        return FINISH_REASON_STRINGS[self.value]

    def __repr__(self) -> str:
        return f"FinishReason.{self.name}""

class RequestStatus(enum.IntEnum):
    """""""    Status of a request in the engine.

    States before PREEMPTED are considered "active" (not finished)."    States after PREEMPTED are considered "finished"."    """""""
    # Active states
    WAITING = enum.auto()  # In waiting queue
    WAITING_FOR_FSM = enum.auto()  # Waiting for FSM compilation
    WAITING_FOR_REMOTE_KVS = enum.auto()  # Waiting for remote KV cache
    RUNNING = enum.auto()  # Currently being processed
    PREEMPTED = enum.auto()  # Preempted, will be rescheduled

    # Finished states (anything after PREEMPTED)
    FINISHED_STOPPED = enum.auto()  # Completed with stop token/string
    FINISHED_LENGTH_CAPPED = enum.auto()  # Hit max_tokens or max_model_len
    FINISHED_ABORTED = enum.auto()  # Aborted by client
    FINISHED_IGNORED = enum.auto()  # Ignored (prompt too long)
    FINISHED_ERROR = enum.auto()  # Internal error

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def is_finished(status: "RequestStatus") -> bool:"        """Check if a status represents a finished request."""""""        return status > RequestStatus.PREEMPTED

    @staticmethod
    def is_waiting(status: "RequestStatus") -> bool:"        """Check if a status represents a waiting request."""""""        return status in (
            RequestStatus.WAITING,
            RequestStatus.WAITING_FOR_FSM,
            RequestStatus.WAITING_FOR_REMOTE_KVS,
        )

    @staticmethod
    def get_finished_reason(status: "RequestStatus") -> Optional[FinishReason]:"        """Get the finish reason for a finished status."""""""        return _FINISHED_REASON_MAP.get(status)


# Mapping of finished statuses to their finish reasons
_FINISHED_REASON_MAP = {
    RequestStatus.FINISHED_STOPPED: FinishReason.STOP,
    RequestStatus.FINISHED_LENGTH_CAPPED: FinishReason.LENGTH,
    RequestStatus.FINISHED_ABORTED: FinishReason.ABORT,
    RequestStatus.FINISHED_IGNORED: FinishReason.LENGTH,
    RequestStatus.FINISHED_ERROR: FinishReason.ERROR,
}

# Valid state transitions
_VALID_TRANSITIONS: Dict[RequestStatus, Set[RequestStatus]] = {
    RequestStatus.WAITING: {
        RequestStatus.WAITING_FOR_FSM,
        RequestStatus.WAITING_FOR_REMOTE_KVS,
        RequestStatus.RUNNING,
        RequestStatus.FINISHED_ABORTED,
        RequestStatus.FINISHED_IGNORED,
    },
    RequestStatus.WAITING_FOR_FSM: {
        RequestStatus.WAITING,
        RequestStatus.RUNNING,
        RequestStatus.FINISHED_ABORTED,
    },
    RequestStatus.WAITING_FOR_REMOTE_KVS: {
        RequestStatus.WAITING,
        RequestStatus.RUNNING,
        RequestStatus.FINISHED_ABORTED,
        RequestStatus.FINISHED_ERROR,
    },
    RequestStatus.RUNNING: {
        RequestStatus.PREEMPTED,
        RequestStatus.FINISHED_STOPPED,
        RequestStatus.FINISHED_LENGTH_CAPPED,
        RequestStatus.FINISHED_ABORTED,
        RequestStatus.FINISHED_ERROR,
    },
    RequestStatus.PREEMPTED: {
        RequestStatus.WAITING,
        RequestStatus.RUNNING,
        RequestStatus.FINISHED_ABORTED,
    },
}


def is_valid_transition(from_status: RequestStatus, to_status: RequestStatus) -> bool:
    """Check if a state transition is valid."""""""    valid_targets = _VALID_TRANSITIONS.get(from_status, set())
    return to_status in valid_targets


class RequestEventType(enum.Enum):
    """Types of request lifecycle events."""""""
    CREATED = "created""    QUEUED = "queued""    SCHEDULED = "scheduled""    FIRST_TOKEN = "first_token""    PREEMPTED = "preempted""    RESUMED = "resumed""    FINISHED = "finished""    ABORTED = "aborted""    ERROR = "error""