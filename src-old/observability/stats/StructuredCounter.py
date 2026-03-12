r"""LLM_CONTEXT_START

## Source: src-old/observability/stats/StructuredCounter.description.md

# StructuredCounter

**File**: `src\observability\stats\StructuredCounter.py`  
**Type**: Python Module  
**Summary**: 6 classes, 2 functions, 9 imports  
**Lines**: 207  
**Complexity**: 11 (moderate)

## Overview

StructuredCounter - Dataclass-based structured metric counters.

Inspired by vLLM's CompilationCounter pattern for tracking detailed metrics
with snapshot/diff capabilities and testing support.

Phase 24: Advanced Observability & Parsing

## Classes (6)

### `StructuredCounter`

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

**Methods** (7):
- `clone(self)`
- `reset(self)`
- `diff(self, other)`
- `as_dict(self)`
- `expect(self)`
- `increment(self, field_name, amount)`
- `decrement(self, field_name, amount)`

### `CompilationCounter`

**Inherits from**: StructuredCounter

Counter for tracking compilation-related metrics.

Based on vLLM's compilation counter pattern.

### `RequestCounter`

**Inherits from**: StructuredCounter

Counter for tracking request-related metrics.

### `CacheCounter`

**Inherits from**: StructuredCounter

Counter for tracking cache-related metrics.

**Methods** (1):
- `hit_ratio(self)`

### `PoolCounter`

**Inherits from**: StructuredCounter

Counter for tracking object pool metrics.

**Methods** (1):
- `active_objects(self)`

### `QueueCounter`

**Inherits from**: StructuredCounter

Counter for tracking queue metrics.

## Functions (2)

### `get_all_counters()`

Get all global counters.

### `reset_all_counters()`

Reset all global counters.

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `contextlib.contextmanager`
- `copy`
- `dataclasses.dataclass`
- `dataclasses.field`
- `dataclasses.fields`
- `typing.Any`
- `typing.Generator`
- `typing.TypeVar`

---
*Auto-generated documentation*
## Source: src-old/observability/stats/StructuredCounter.improvements.md

# Improvements for StructuredCounter

**File**: `src\observability\stats\StructuredCounter.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 207 lines (medium)  
**Complexity**: 11 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StructuredCounter_test.py` with pytest tests

### Code Organization
- [TIP] **6 classes in one file** - Consider splitting into separate modules

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

"""
StructuredCounter - Dataclass-based structured metric counters.

Inspired by vLLM's CompilationCounter pattern for tracking detailed metrics
with snapshot/diff capabilities and testing support.

Phase 24: Advanced Observability & Parsing
"""


import copy
from contextlib import contextmanager
from dataclasses import dataclass, fields
from typing import Any, Generator, TypeVar

T = TypeVar("T", bound="StructuredCounter")


@dataclass
class StructuredCounter:
    """Base class for structured metric counters.

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
        for f in fields(self):
            if f.default is not f.default_factory:
                setattr(self, f.name, f.default if f.default is not dataclass else 0)
            elif f.default_factory is not dataclass:
                setattr(self, f.name, f.default_factory())
            else:
                setattr(self, f.name, 0)

    def diff(self: T, other: T) -> dict[str, int]:
        """Compute the difference between this counter and another.

        Args:
            other: The baseline counter to compare against

        Returns:
            Dictionary of field names to their differences (self - other)

        """
        result = {}
        for f in fields(self):
            current = getattr(self, f.name)
            baseline = getattr(other, f.name)
            if isinstance(current, (int, float)) and isinstance(baseline, (int, float)):
                diff = current - baseline
                if diff != 0:
                    result[f.name] = diff
        return result

    def as_dict(self) -> dict[str, Any]:
        """Convert counter to dictionary."""
        return {f.name: getattr(self, f.name) for f in fields(self)}

    @contextmanager
    def expect(self, **kwargs: int) -> Generator[None, None, None]:
        """Context manager for testing expected counter changes.

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
        for name, expected_diff in kwargs.items():
            actual_diff = getattr(self, name) - getattr(old, name)
            assert actual_diff == expected_diff, (
                f"{name} not as expected: before={getattr(old, name)}, "
                f"after={getattr(self, name)}, expected_diff={expected_diff}, "
                f"actual_diff={actual_diff}"
            )

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
    """Counter for tracking compilation-related metrics.

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
