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

"""
Enums.py module.
"""

# SPDX-License-Identifier: Apache-2.0
from enum import Enum, auto


class CacheGroupType(Enum):
    """Type of KV cache group."""

    FULL_ATTENTION = auto()
    SLIDING_WINDOW = auto()
    CROSS_ATTENTION = auto()
    CHUNKED_LOCAL = auto()
    MLA_COMPRESSED = auto()
    PACKKV_COMPRESSED = auto()


class AllocationStrategy(Enum):
    """Block allocation strategy."""

    GREEDY = auto()  # Allocate as needed
    PREDICTIVE = auto()  # Pre-allocate based on expected length
    CONSERVATIVE = auto()  # Minimal allocation, grow on demand
    ADAPTIVE = auto()  # Adjust based on memory pressure


class EvictionPolicy(Enum):
    """Block eviction policy."""

    LRU = auto()  # Least recently used
    ARC = auto()  # Adaptive replacement cache
    PRIORITY = auto()  # Priority-based eviction
    FREQUENCY = auto()  # Least frequently used
