#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple
import time

@dataclass
class RecordedInteraction:
    """A recorded test interaction.

    Attributes:
        call_type: Type of call (e.g., "api", "file", "db").
        call_name: Name of the call.
        args: Call arguments.
        kwargs: Call keyword arguments.
        result: Call result.
        timestamp: When recorded.
    """

    call_type: str
    call_name: str
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = field(default_factory=lambda: {})
    result: Any = None
    timestamp: float = field(default_factory=time.time)
