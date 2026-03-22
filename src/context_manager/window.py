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

"""Context window — a labelled, token-aware sliding context with metadata.

Extends the base :class:`~context_manager.ContextManager` with per-segment
metadata, priority weighting and serialisation support.  This is the primary
context abstraction used by LLM prompt builders.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextSegment:
    """A single labelled text segment stored in a :class:`ContextWindow`.

    Parameters
    ----------
    text:
        The raw text content.
    label:
        Short human-readable label (e.g. ``"user"``, ``"assistant"``, ``"system"``).
    priority:
        Higher priority segments survive pruning longer (default ``1``).
    created_at:
        Unix timestamp when the segment was created (default: current time).
    metadata:
        Arbitrary key/value metadata (e.g. turn id, source agent).
    """

    text: str
    label: str = "text"
    priority: int = 1
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def token_count(self) -> int:
        """Approximate token count (whitespace-split word count)."""
        return len(self.text.split())

    def to_dict(self) -> dict[str, Any]:
        """Serialise the segment to a plain dictionary."""
        return {
            "text": self.text,
            "label": self.label,
            "priority": self.priority,
            "created_at": self.created_at,
            "token_count": self.token_count,
            "metadata": dict(self.metadata),
        }


class ContextWindow:
    """A token-budget, priority-aware sliding window for LLM contexts.

    Segments are pruned from the *lowest-priority, oldest* end when the
    aggregate token count would exceed *max_tokens*.  Ties in priority are
    broken by age (oldest pruned first).

    Parameters
    ----------
    max_tokens:
        Maximum total (whitespace) token count across all segments.
    """

    def __init__(self, max_tokens: int) -> None:
        self._segments: list[ContextSegment] = []
        self.max_tokens = max_tokens

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def segments(self) -> list[ContextSegment]:
        """Current list of segments (oldest first)."""
        return list(self._segments)

    @property
    def token_count(self) -> int:
        """Total token count across all segments."""
        return sum(s.token_count for s in self._segments)

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    async def push(
        self,
        text: str,
        *,
        label: str = "text",
        priority: int = 1,
        metadata: dict[str, Any] | None = None,
    ) -> ContextSegment:
        """Add a new segment and prune the window if needed.

        Pruning removes the lowest-priority, oldest segment(s) until the
        token budget is satisfied.

        Parameters
        ----------
        text:
            Raw text to add.
        label:
            Role/label for this segment.
        priority:
            Retention priority (higher = pruned later).
        metadata:
            Optional key/value annotations.

        Returns
        -------
        ContextSegment
            The created segment.
        """
        seg = ContextSegment(
            text=text,
            label=label,
            priority=priority,
            metadata=metadata or {},
        )
        self._segments.append(seg)
        await self._prune()
        return seg

    def snapshot(self) -> str:
        """Return all segment text joined in order."""
        return "".join(s.text for s in self._segments)

    def clear(self) -> None:
        """Remove all segments."""
        self._segments.clear()

    def to_dict(self) -> dict[str, Any]:
        """Serialise the window state."""
        return {
            "max_tokens": self.max_tokens,
            "token_count": self.token_count,
            "segments": [s.to_dict() for s in self._segments],
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _prune(self) -> None:
        """Remove segments until token_count <= max_tokens."""
        while self.token_count > self.max_tokens and self._segments:
            # Find the lowest-priority, oldest segment to evict
            # Sort key: (priority ASC, created_at ASC) → first in sort order = evict
            victim_idx = min(
                range(len(self._segments)),
                key=lambda i: (self._segments[i].priority, self._segments[i].created_at),
            )
            self._segments.pop(victim_idx)
