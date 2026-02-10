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
StructuredCounter - Dataclass-based structured metric counters.

Inspired by vLLM's CompilationCounter pattern for tracking detailed metrics
with snapshot/diff capabilities and testing support.

Phase 24: Advanced Observability & Parsing
"""

from __future__ import annotations

import copy
import functools
from contextlib import contextmanager
from dataclasses import dataclass, fields
from typing import Any, Generator, TypeVar

T = TypeVar("T", bound="StructuredCounter")


@dataclass
class StructuredCounter:
    """
    Base class for structured metric counters.

    Provides snapshot, diff, and testing utilities for tracking
    detailed metrics across operations.

    Usage:
        @dataclass
        class MyCounter(StructuredCounter):
            requests_processed: int = 0
            cache_hits: int = 0
            cache_misses: int = 0

        counter = MyCounter()
        counter.requests_processed += 1

        # Test expected changes
        with counter.expect(requests_processed=1, cache_hits=1):
            counter.requests_processed += 1
            counter.cache_hits += 1
    """

    def clone(self: T) -> T:
        """Create a deep copy of this counter."""
        return copy.deepcopy(self)

    def reset(self) -> None:
        """Reset all counter fields to their default values."""
        def reset_field(f: Any) -> None:
            if f.default is not f.default_factory:
                setattr(self, f.name, f.default if f.default is not dataclass else 0)
            elif f.default_factory is not dataclass:
                setattr(self, f.name, f.default_factory())
            else:
                setattr(self, f.name, 0)

        list(map(reset_field, fields(self)))

    def diff(self: T, other: T) -> dict[str, int]:
        """
        Compute the difference between this counter and another.

        Args:
            other: The baseline counter to compare against

        Returns:
            Dictionary of field names to their differences (self - other)
        """
        def calculate_diff(acc: dict[str, int], f: Any) -> dict[str, int]:
            current = getattr(self, f.name)
            baseline = getattr(other, f.name)
            if isinstance(current, (int, float)) and isinstance(baseline, (int, float)):
                diff_val = current - baseline
                if diff_val != 0:
                    acc[f.name] = diff_val
            return acc

        return functools.reduce(calculate_diff, fields(self), {})

    def as_dict(self) -> dict[str, Any]:
        """Convert counter to dictionary regarding current values."""
        return {f.name: getattr(self, f.name) for f in fields(self)}

    @contextmanager
    def expect(self, **kwargs: int) -> Generator[None, None, None]:
        """
        Context manager for testing expected counter changes.

        Args:
            **kwargs: Expected changes for each counter field

        Raises:
            AssertionError: If actual changes don't match expected

        Example:
            with counter.expect(cache_hits=2, cache_misses=1):
                # ... code that should increment cache_hits by 2, cache_misses by 1
        """
        old = self.clone()
        yield

        def check_expected(item: tuple[str, int]) -> None:
            name, expected_diff = item
            actual_diff = getattr(self, name) - getattr(old, name)
            assert actual_diff == expected_diff, (
                f"{name} not as expected: before={getattr(old, name)}, "
                f"after={getattr(self, name)}, expected_diff={expected_diff}, "
                f"actual_diff={actual_diff}"
            )

        list(map(check_expected, kwargs.items()))

    def increment(self, field_name: str, amount: int = 1) -> None:
        """Increment a counter field by the given amount."""
        current = getattr(self, field_name)
        setattr(self, field_name, current + amount)

    def decrement(self, field_name: str, amount: int = 1) -> None:
        """Decrement a counter field by the given amount."""
        current = getattr(self, field_name)
        setattr(self, field_name, current - amount)


@dataclass
class CompilationCounter(StructuredCounter):
    """
    Counter for tracking compilation-related metrics.

    Based on vLLM's compilation counter pattern.
    """

    num_models_seen: int = 0
    num_graphs_seen: int = 0
    num_piecewise_graphs_seen: int = 0
    num_piecewise_capturable_graphs_seen: int = 0
    num_backend_compilations: int = 0
    num_cache_entries_updated: int = 0
    num_compiled_artifacts_saved: int = 0


@dataclass
class RequestCounter(StructuredCounter):
    """Counter for tracking request-related metrics."""

    requests_received: int = 0
    requests_completed: int = 0
    requests_failed: int = 0
    requests_cancelled: int = 0
    requests_timeout: int = 0
    tokens_generated: int = 0
    tokens_input: int = 0


@dataclass
class CacheCounter(StructuredCounter):
    """Counter for tracking cache-related metrics."""

    cache_hits: int = 0
    cache_misses: int = 0
    cache_evictions: int = 0
    cache_insertions: int = 0
    cache_size: int = 0

    @property
    def hit_ratio(self) -> float:
        """Compute cache hit ratio."""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0


@dataclass
class PoolCounter(StructuredCounter):
    """Counter for tracking object pool metrics."""

    objects_acquired: int = 0
    objects_released: int = 0
    objects_created: int = 0
    objects_destroyed: int = 0
    pool_size: int = 0
    pool_capacity: int = 0

    @property
    def active_objects(self) -> int:
        """Number of objects currently in use."""
        return self.objects_acquired - self.objects_released


@dataclass
class QueueCounter(StructuredCounter):
    """Counter for tracking queue metrics."""

    items_enqueued: int = 0
    items_dequeued: int = 0
    items_dropped: int = 0
    queue_size: int = 0
    max_queue_size: int = 0


# Global counters
compilation_counter = CompilationCounter()
request_counter = RequestCounter()
cache_counter = CacheCounter()


def get_all_counters() -> dict[str, StructuredCounter]:
    """Get all global counters."""
    return {
        "compilation": compilation_counter,
        "request": request_counter,
        "cache": cache_counter,
    }


def reset_all_counters() -> None:
    """Reset all global counters."""
    compilation_counter.reset()
    request_counter.reset()
    cache_counter.reset()
