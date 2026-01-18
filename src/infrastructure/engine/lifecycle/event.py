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
