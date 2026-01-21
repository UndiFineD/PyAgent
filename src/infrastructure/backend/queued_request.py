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


"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from dataclasses import dataclass
from collections.abc import Callable

__version__ = VERSION


@dataclass
class QueuedRequest:
    """A request waiting in the queue.

    Attributes:
        priority: Request priority (higher=more urgent).
        timestamp: When request was queued.
        request_id: Unique request identifier.
        prompt: The prompt to send.
        callback: Optional callback function.
    """

    priority: int
    timestamp: float
    request_id: str
    prompt: str
    callback: Callable[[str], None] | None = None

    def __lt__(self, other: QueuedRequest) -> bool:
        """Compare by priority (descending) then timestamp (ascending)."""
        if self.priority != other.priority:
            return self.priority > other.priority  # Higher priority first
        return self.timestamp < other.timestamp  # Earlier first
