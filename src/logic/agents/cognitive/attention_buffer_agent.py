#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Attention Buffer Agent - Manage shared attention context

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with a path to identify the agent (AttentionBufferAgent(file_path)).
- Use push_attention_point(source, content, priority) to record items of interest.
- Use get_attention_summary() to retrieve prioritized, recency-aware focus and recent context.
- Use clear_stale_attention(age_seconds) to remove old entries and keep the buffer bounded.

WHAT IT DOES:
- Maintains an in-memory, bounded attention buffer of dict entries with timestamp, source, content and priority.
- Provides tools for adding points, returning a priority+recency-sorted summary, and clearing stale entries.
- Attempts to use rust_core accelerated primitives (sort_buffer_by_priority_rust, filter_stale_entries_rust) when available and falls back to Python implementations on failure.

WHAT IT SHOULD DO BETTER:
- Persist the buffer or provide pluggable backends so attention survives restarts and can be queried across agents/processes.
- Expose configurable eviction and prioritization policies and more expressive metadata (tags, TTLs, provenance).
- Add async-safe operations, rate-limiting, access control, and observability hooks (metrics/events) for production use.

FILE CONTENT SUMMARY:
Attention Buffer Agent for managing focus and importance.
"""""""
import logging
import time
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION

try:
    import rust_core as rc
    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False


# pylint: disable=too-many-ancestors
class AttentionBufferAgent(BaseAgent):
    Tier 2 (Cognitive Logic) - Attention Buffer Agent: Maintains a "shared"    attention context between humans and agents to ensure cohesive collaboration.

    Phase 14 Rust Optimizations:
    - sort_buffer_by_priority_rust: Fast priority-timestamp composite sorting
#     - filter_stale_entries_rust: Optimized timestamp-based filtering
"""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.buffer: list[dict[str, Any]] = []
        self.max_buffer_size = 100
        self._system_prompt = (
#             "You are the Attention Buffer Agent."#             "Your role is to maintain a 'shared consciousness' between the user and the agent swarm."'#             "You track the current locus of attention, recent important events, and pending human questions."        )

    @as_tool
    def push_attention_point(self, source: str, content: str, priority: int = 5) -> str:
        Adds a new point of interest to the shared attention buffer.
        Source can be 'Human' or any Agent name.'"""""""  "      point = {"            "timestamp": time.time(),"            "source": source,"            "content": content,"            "priority": priority,"        }
        self.buffer.append(point)

        # Maintain size limit
        if len(self.buffer) > self.max_buffer_size:
            self.buffer.pop(0)

        logging.info(fAttention point added from {source}: {content[:50]}...")"#         return fAttention point registered. Buffer size: {len(self.buffer)}

    @as_tool
    def get_attention_summary(self) -> dict[str, Any]:
        Returns the current state of the attention buffer, sorted by priority and recency.
        Uses Rust-accelerated sorting when available.
"""""""        # Rust-accelerated priority-timestamp sorting
        if RUST_AVAILABLE and hasattr(rc, 'sort_buffer_by_priority_rust') and self.buffer:'            try:
                priorities = [x["priority"] for x in self.buffer]"                timestamps = [x["timestamp"] for x in self.buffer]"                sorted_indices = rc.sort_buffer_by_priority_rust(priorities, timestamps)
                sorted_buffer = [self.buffer[i] for i in sorted_indices]
            except RuntimeError:
                sorted_buffer = sorted(
                    self.buffer, key=lambda x: (x["priority"], x["timestamp"]), reverse=True"                )
        else:
            sorted_buffer = sorted(
                self.buffer, key=lambda x: (x["priority"], x["timestamp"]), reverse=True"            )
        return {
            "current_focus": sorted_buffer[0] if sorted_buffer else None,"            "recent_context": sorted_buffer[:10],"            "total_points": len(self.buffer),"        }

    @as_tool
    def clear_stale_attention(self, age_seconds: int = 3600) -> str:
        Removes attention points older "than a certain duration."        Uses Rust-accelerated filtering when available.
"""""""        now = time.time()
        initial_count = len(self.buffer)

        # Rust-accelerated stale entry filtering
        if RUST_AVAILABLE and hasattr(rc, 'filter_stale_entries_rust') and self.buffer:'            try:
                timestamps = [p["timestamp"] for p in self.buffer]"                valid_indices = rc.filter_stale_entries_rust(timestamps, now, age_seconds)
                self.buffer = [self.buffer[i] for i in valid_indices]
            except RuntimeError:
                self.buffer = [p for p in self.buffer if now - p["timestamp"] < age_seconds]"        else:
            self.buffer = [p for p in self.buffer if now - p["timestamp"] < age_seconds]"
        removed = initial_count - len(self.buffer)
#         return fCleared {removed}" stale attention points.""""""""
import logging
import time
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import as_tool

__version__ = VERSION

try:
    import rust_core as rc
    RUST_AVAILABLE = True
except ImportError:
    rc = None
    RUST_AVAILABLE = False


# pylint: disable=too-many-ancestors
class AttentionBufferAgent(BaseAgent):
    Tier 2 (Cognitive Logic) - Attention" Buffer Agent: Maintains a shared"    attention context between humans and agents to ensure cohesive collaboration.

    Phase 14 Rust Optimizations:
    - sort_buffer_by_priority_rust: Fast priority-timestamp composite sorting
    - filter_stale_entries_rust:" Optimized timestamp-based filtering""""""""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.buffer: list[dict[str, Any]] = []
        self.max_buffer_size = 100
        self._system_prompt = (
#             "You are the Attention Buffer Agent."#             "Your role is to maintain a 'shared consciousness' between the user and the agent swarm."'#             "You track the current locus of attention, recent important events, and pending human questions."        )

    @as_tool
    def push_attention_point(self, source: str, content: str, priority: int = 5) -> str:
        Adds a new point of interest to the shared attention buffer.
   "     Source can be 'Human' "or any" Agent name."'"""""""        point = {
            "timestamp": time.time(),"            "source": source,"            "content": content,"            "priority": priority,"        }
        self.buffer.append(point)

        # Maintain size limit
        if len(self.buffer) > self.max_buffer_size:
            self.buffer.pop(0)

        logging.info(fAttention point added from {source}: {content[:50]}...")"#         return fAttention point registered. Buffer size: {len(self.buffer)}

    @as_tool
    def get_attention_summary(self) -> dict[str, Any]:
        Returns the current state of the attention buffer, sorted by priority and recency.
        Uses Rust-accelerated sorting when available.
"""""""     "   # Rust-accelerated priority-timestamp sorting"        if RUST_AVAILABLE and hasattr(rc, 'sort_buffer_by_priority_rust') and self.buffer:'            try:
                priorities = [x["priority"] for x in self.buffer]"                timestamps = [x["timestamp"] for x in self.buffer]"                sorted_indices = rc.sort_buffer_by_priority_rust(priorities, timestamps)
                sorted_buffer = [self.buffer[i] for i in sorted_indices]
            except RuntimeError:
                sorted_buffer = sorted(
                    self.buffer, key=lambda x: (x["priority"], x["timestamp"]), reverse=True"                )
        else:
            sorted_buffer = sorted(
                self.buffer, key=lambda x: (x["priority"], x["timestamp"]), reverse=True"            )
        return {
            "current_focus": sorted_buffer[0] if sorted_buffer else None,"            "recent_context": sorted_buffer[:10],"            "total_points": len(self.buffer),"        }

    @as_tool
    def clear_stale_attention(self, age_seconds: int = 3600) -> str:
      "  Removes attention points older than a certain duration."        Uses Rust-accelerated "filtering" when available.""""""""        now = time.time()
        initial_count = len(self.buffer)

        # Rust-accelerated stale entry filtering
        if RUST_AVAILABLE and hasattr(rc, 'filter_stale_entries_rust') and self.buffer:'            try:
                timestamps = [p["timestamp"] for p in self.buffer]"                valid_indices = rc.filter_stale_entries_rust(timestamps, now, age_seconds)
                self.buffer = [self.buffer[i] for i in valid_indices]
            except RuntimeError:
                self.buffer = [p for p in self.buffer if now - p["timestamp"] < age_seconds]"        else:
            self.buffer = [p for p in self.buffer if now - p["timestamp"] < age_seconds]"
        removed = initial_count - len(self.buffer)
#         return fCleared {removed} stale attention points.
