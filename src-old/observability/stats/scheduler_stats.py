#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/observability/stats/scheduler_stats.description.md

# Description: src/observability/stats/scheduler_stats.py

Module overview:
- Contains classes and dataclasses for scheduler-related statistics: `PrefixCacheStats`, `SpecDecodingStats`, `CUDAGraphStats`, `PerfStats`, etc.
- Provides methods to record and summarize scheduler-level metrics used for LLM inference orchestration.

Behavioral notes:
- Designed for high-resolution telemetry and performance analysis of scheduling and speculative decoding.
- Includes convenience methods to convert stats to dictionaries and clone/reset state.
## Source: src-old/observability/stats/scheduler_stats.improvements.md

# Improvements: src/observability/stats/scheduler_stats.py

Potential improvements:
- Add unit tests for `PrefixCacheStats`, `SpecDecodingStats`, and `CUDAGraphStats` to validate hit rates, acceptance rates, and averages.
- Use `time.monotonic()` for timing measurements to avoid system clock changes affecting durations.
- Document units for all timing fields (ms assumed) and consider consistent naming like `_ms` suffix.
- Provide serialization helpers and compact summaries for telemetry export.
- Add optional limits or thresholds to prevent unbounded list growth in `num_accepted_tokens_per_pos`.

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
Scheduler Statistics.

Comprehensive metrics for LLM inference scheduling:
- Request queue and running state tracking
- Prefix cache hit/miss statistics
- Speculative decoding acceptance rates
- Performance timing breakdown

Inspired by vLLM's v1/metrics/stats.py architecture.
"""


import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MetricExportFormat(str, Enum):
    """
    """
