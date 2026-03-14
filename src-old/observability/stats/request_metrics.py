#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/stats/request_metrics.description.md

# Description: src/observability/stats/request_metrics.py

Module overview:
- Implements `RequestMetrics` dataclass and `RequestState` enum used to track detailed timing and state transitions for requests.
- Provides methods to mark lifecycle events (queued, scheduled, processing, first token, completed, failed) and computed timing properties (ms).

Primary types:
- `RequestState` (Enum)
- `RequestMetrics` (dataclass)

Behavioral notes:
- Designed for high-resolution latency analysis; includes convenience methods for marking events and computed properties for different timing buckets.
## Source: src-old/observability/stats/request_metrics.improvements.md

# Improvements: src/observability/stats/request_metrics.py

Potential improvements:
- Add unit tests that validate timing property calculations across controlled timestamps (use monkeypatch for time.time).
- Ensure numeric units are documented (ms vs seconds) and consistent.
- Add serialization helpers for logging metrics snapshots.
- Consider using monotonic clocks (`time.monotonic()`) for duration calculations to avoid issues with system clock adjustments.
- Add doc examples for typical usage in request lifecycle instrumentation.

LLM_CONTEXT_END
"""
from __future__ import annotations


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
RequestMetrics - Comprehensive timing breakdown for request processing.

Inspired by vLLM's sequence.py RequestMetrics for production latency analysis.

Phase 17: vLLM Pattern Integration
"""


import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class RequestState(Enum):
    """
    """
