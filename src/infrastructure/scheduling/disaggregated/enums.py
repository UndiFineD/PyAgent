# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from enum import Enum, auto

class InstanceRole(Enum):
    """Role of a vLLM instance in disaggregated serving."""
    PREFILL = auto()     # Handles prefill phase only
    DECODE = auto()      # Handles decode phase only
    UNIFIED = auto()     # Handles both (traditional mode)


class SchedulingPolicy(Enum):
    """Request routing policy for multi-instance deployment."""
    ROUND_ROBIN = auto()         # Simple rotation
    LEAST_LOADED = auto()        # Route to least busy instance
    RANDOM = auto()              # Random selection
    HASH_BASED = auto()          # Hash request ID for consistency
    LATENCY_AWARE = auto()       # Route to lowest latency instance
