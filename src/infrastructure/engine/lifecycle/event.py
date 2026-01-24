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
"""Request lifecycle events."""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .enums import RequestEventType


@dataclass
class RequestEvent:
    """
    A timestamped event in the request lifecycle.

    Attributes:
        event_type: Type of the event
        timestamp: Unix timestamp when the event occurred
        details: Optional additional information about the event
    """

    event_type: RequestEventType
    timestamp: float = field(default_factory=time.time)
    details: Optional[Dict[str, Any]] = None

    @classmethod
    def new_event(
        cls,
        event_type: RequestEventType,
        timestamp: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> "RequestEvent":
        """Factory method to create a new event."""
        return cls(
            event_type=event_type,
            timestamp=timestamp if timestamp is not None else time.time(),
            details=details,
        )
