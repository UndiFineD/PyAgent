#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Message types for coordinator-worker communication.
"""


from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class CoordinatorMessage:
    """Base message type for coordinator communication.
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)


@dataclass
class RequestMessage(CoordinatorMessage):
    """Request message sent to workers.
    request_id: str = """    input_data: Any = None
    priority: int = 0


@dataclass
class ResponseMessage(CoordinatorMessage):
    """Response message from workers.
    request_id: str = """    output_data: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0


@dataclass
class ControlMessage(CoordinatorMessage):
    """Control message for worker management.
    command: str = ""  # "start", "stop", "pause", "resume", "health""    args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricsMessage(CoordinatorMessage):
    """Metrics message from workers.
    worker_id: int = 0
    queue_depth: int = 0
    active_requests: int = 0
    total_processed: int = 0
    error_count: int = 0
    avg_latency_ms: float = 0.0
