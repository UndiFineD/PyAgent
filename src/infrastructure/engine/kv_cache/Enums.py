# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto

class CacheGroupType(Enum):
    """Type of KV cache group."""
    FULL_ATTENTION = auto()
    SLIDING_WINDOW = auto()
    CROSS_ATTENTION = auto()
    CHUNKED_LOCAL = auto()
    MLA_COMPRESSED = auto()


class AllocationStrategy(Enum):
    """Block allocation strategy."""
    GREEDY = auto()         # Allocate as needed
    PREDICTIVE = auto()     # Pre-allocate based on expected length
    CONSERVATIVE = auto()   # Minimal allocation, grow on demand
    ADAPTIVE = auto()       # Adjust based on memory pressure


class EvictionPolicy(Enum):
    """Block eviction policy."""
    LRU = auto()           # Least recently used
    ARC = auto()           # Adaptive replacement cache
    PRIORITY = auto()      # Priority-based eviction
    FREQUENCY = auto()     # Least frequently used
