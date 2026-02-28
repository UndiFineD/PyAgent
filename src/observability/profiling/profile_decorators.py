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
ProfileDecorators - cProfile-based profiling utilities.

Inspired by vLLM's profiling.py patterns for ad-hoc profiling.

Provides decorators and context managers for profiling Python code
with cProfile, integrated with RustProfiler for unified reporting.

Phase 17: vLLM Pattern Integration (P2)
"""

from __future__ import annotations

import cProfile
import functools
import io
import pstats
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class ProfileResult:
    """Result from a profiling session."""

    name: str
    elapsed_seconds: float
    stats: pstats.Stats | None = None
    call_count: int = 0
    top_functions: list[tuple[str, float]] = field(default_factory=list)

    def summary(self) -> dict:
        """Generate a summary dict."""
        return {
            "name": self.name,
            "elapsed_seconds": round(self.elapsed_seconds, 4),
            "elapsed_ms": round(self.elapsed_seconds * 1000, 2),
            "call_count": self.call_count,
            "top_functions": self.top_functions[:10],
        }

    def print_stats(self, limit: int = 20) -> None:
        """Print profiling statistics."""
        if self.stats:
            print(f"\n=== Profile: {self.name} ({self.elapsed_seconds * 1000:.2f}ms) ===")
            self.stats.sort_stats("cumulative")
            self.stats.print_stats(limit)


@contextmanager
def cprofile_context(
    enabled: bool = True,
    output_file: str | Path | None = None,
    print_stats: bool = False,
    limit: int = 20,
) -> Iterator[ProfileResult]:
    """
    Context manager for cProfile profiling.

    Args:
        enabled: Whether profiling is enabled
        output_file: Optional file to save stats
        print_stats: Whether to print stats on exit
        limit: Number of top functions to show

    Yields:
        ProfileResult with timing and stats

    Example:
        >>> with cprofile_context(print_stats=True) as result:
        ...     expensive_operation()
        >>> print(f"Took {result.elapsed_ms}ms")
    """
    result = ProfileResult(name="profile", elapsed_seconds=0.0)

    if not enabled:
        start = time.perf_counter()
        try:
            yield result
        finally:
            result.elapsed_seconds = time.perf_counter() - start
        return

    profiler = cProfile.Profile()
    start = time.perf_counter()

    try:
        profiler.enable()
        yield result
    finally:
        profiler.disable()
        result.elapsed_seconds = time.perf_counter() - start

        # Capture stats
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        result.stats = stats

        # Count total calls
        for (filename, line, name), (cc, nc, tt, ct, callers) in stats.stats.items():
            result.call_count += nc

        # Extract top functions by cumulative time
        stats.sort_stats("cumulative")
        for (filename, line, name), (cc, nc, tt, ct, callers) in list(stats.stats.items())[:limit]:
            func_name = f"{name} ({Path(filename).name}:{line})"
            result.top_functions.append((func_name, ct))

        if output_file:
            stats.dump_stats(str(output_file))

        if print_stats:
            result.print_stats(limit)


def cprofile(
    enabled: bool = True,
    output_file: str | Path | None = None,
    print_stats: bool = False,
    limit: int = 20,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for cProfile profiling.

    Args:
        enabled: Whether profiling is enabled
        output_file: Optional file to save stats
        print_stats: Whether to print stats after call
        limit: Number of top functions to show

    Returns:
        Decorated function

    Example:
        >>> @cprofile(print_stats=True)
        ... def slow_function():
        ...     time.sleep(0.1)
        >>> slow_function()
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with cprofile_context(
                enabled=enabled,
                output_file=output_file,
                print_stats=print_stats,
                limit=limit,
            ) as result:
                result.name = func.__name__
                return func(*args, **kwargs)

        return wrapper

    return decorator


@contextmanager
def timer_context(name: str = "operation") -> Iterator[dict]:
    """
    Simple timing context manager.

    Args:
        name: Name for the timed operation

    Yields:
        Dict with timing info (populated on exit)

    Example:
        >>> with timer_context("data_load") as timing:
        ...     data = load_data()
        >>> print(f"Took {timing['elapsed_ms']:.2f}ms")
    """
    timing = {"name": name, "start": 0.0, "end": 0.0, "elapsed_seconds": 0.0, "elapsed_ms": 0.0}
    timing["start"] = time.perf_counter()
    try:
        yield timing
    finally:
        timing["end"] = time.perf_counter()
        timing["elapsed_seconds"] = timing["end"] - timing["start"]
        timing["elapsed_ms"] = timing["elapsed_seconds"] * 1000


def timer(name: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Simple timing decorator.

    Args:
        name: Optional name (defaults to function name)

    Returns:
        Decorated function that prints timing

    Example:
        >>> @timer()
        ... def slow_function():
        ...     time.sleep(0.1)
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        operation_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with timer_context(operation_name) as timing:
                result = func(*args, **kwargs)
            print(f"[TIMER] {operation_name}: {timing['elapsed_ms']:.2f}ms")
            return result

        return wrapper

    return decorator


class ProfileAccumulator:
    """
    Accumulates profiling data across multiple calls.

    Useful for tracking function performance over time.

    Example:
        >>> acc = ProfileAccumulator()
        >>>
        >>> @acc.track
        ... def my_function():
        ...     pass
        >>>
        >>> for _ in range(100):
        ...     my_function()
        >>>
        >>> print(acc.report())
    """

    def __init__(self) -> None:
        self._data: dict[str, list[float]] = {}

    def record(self, name: str, elapsed_seconds: float) -> None:
        """Record a timing."""
        if name not in self._data:
            self._data[name] = []
        self._data[name].append(elapsed_seconds)

    def track(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorator to track a function's timing."""

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                self.record(func.__name__, elapsed)

        return wrapper

    def report(self) -> dict[str, dict[str, float]]:
        """Generate a report of all tracked functions."""
        report = {}
        for name, times in self._data.items():
            if times:
                report[name] = {
                    "count": len(times),
                    "total_ms": sum(times) * 1000,
                    "avg_ms": (sum(times) / len(times)) * 1000,
                    "min_ms": min(times) * 1000,
                    "max_ms": max(times) * 1000,
                }
        return report

    def reset(self) -> None:
        """Reset all accumulated data."""
        self._data.clear()

    def print_report(self) -> None:
        """Print the report."""
        print("\n=== Profile Accumulator Report ===")
        for name, stats in self.report().items():
            print(f"{name}:")
            print(f"  calls: {stats['count']}")
            print(f"  total: {stats['total_ms']:.2f}ms")
            print(f"  avg:   {stats['avg_ms']:.2f}ms")
            print(f"  min:   {stats['min_ms']:.2f}ms")
            print(f"  max:   {stats['max_ms']:.2f}ms")


# Global accumulator for ad-hoc profiling
_global_accumulator = ProfileAccumulator()


def track(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator to track function timing in global accumulator."""
    return _global_accumulator.track(func)


def get_profile_report() -> dict:
    """Get report from global accumulator."""
    return _global_accumulator.report()


def reset_profile_data() -> None:
    """Reset global accumulator."""
    _global_accumulator.reset()


__all__ = [
    "ProfileResult",
    "cprofile_context",
    "cprofile",
    "timer_context",
    "timer",
    "ProfileAccumulator",
    "track",
    "get_profile_report",
    "reset_profile_data",
]
