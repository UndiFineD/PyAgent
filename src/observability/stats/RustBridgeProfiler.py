# Copyright 2026 PyAgent Authors
# Rust Bridge Profiler: Comprehensive metadata tracking for Rust-accelerated functions.

from __future__ import annotations
import time
import logging
from collections import defaultdict
from typing import Any, Dict, Callable

try:
    import rust_core
    _RUST_AVAILABLE = True
except ImportError:
    rust_core = None
    _RUST_AVAILABLE = False


class RustBridgeProfiler:
    """
    Orchestrates the profiling of the rust_core.pyd binary.
    Collects execution counts and timing metrics for all exported Rust functions.
    """

    def __init__(self) -> None:
        self.stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"calls": 0, "total_ns": 0})
        self._is_active = False

    def enable(self) -> None:
        """Monkey-patches rust_core functions with profiling wrappers."""
        if not _RUST_AVAILABLE or self._is_active:
            return

        for name in dir(rust_core):
            if not name.startswith("_"):
                func = getattr(rust_core, name)
                if callable(func):
                    setattr(rust_core, name, self._wrap_function(func, name))

        self._is_active = True
        logging.info("RustBridgeProfiler: Enabled (High-precision profiling active).")

    def _wrap_function(self, fn: Callable, fname: str) -> Callable:
        """Wraps a function with nanosecond-precision timing."""
        def wrapper(*args, **kwargs):
            start = time.perf_counter_ns()
            try:
                result = fn(*args, **kwargs)
                duration = time.perf_counter_ns() - start
                self.stats[fname]["calls"] += 1
                self.stats[fname]["total_ns"] += duration
                return result
            except Exception as e:
                # Still record the time even if it failed
                duration = time.perf_counter_ns() - start
                self.stats[fname]["calls"] += 1
                self.stats[fname]["total_ns"] += duration
                raise e
        return wrapper

    def get_report(self) -> str:
        """Generates a markdown report of the profiling results."""
        if not self.stats:
            return "No profiling data collected."

        sorted_stats = sorted(self.stats.items(), key=lambda x: x[1]["total_ns"], reverse=True)
        total_calls = sum(s["calls"] for _, s in sorted_stats)
        total_time_ms = sum(s["total_ns"] for _, s in sorted_stats) / 1e6

        report = [
            "## 🦀 Rust Bridge Profiling Report",
            f"- **Functions Profiled**: {len(sorted_stats)}",
            f"- **Total Invocations**: {total_calls}",
            f"- **Cumulative Execution Time**: {total_time_ms:.3f} ms",
            "",
            "| Function | Calls | Total (ms) | Avg (μs) |",
            "| :--- | :---: | :---: | :---: |"
        ]

        for name, s in sorted_stats:
            avg_us = (s["total_ns"] / s["calls"]) / 1000 if s["calls"] > 0 else 0
            report.append(f"| `{name}` | {s['calls']} | {s['total_ns']/1e6:.3f} | {avg_us:.2f} |")

        return "\n".join(report)

    def log_summary(self) -> None:
        """Logs a summary of the top 5 most expensive functions."""
        if not self.stats:
            return

        sorted_stats = sorted(self.stats.items(), key=lambda x: x[1]["total_ns"], reverse=True)
        logging.info("RustBridgeProfiler: Pulse check complete.")
        for name, s in sorted_stats[:5]:
            avg_us = (s["total_ns"] / s["calls"]) / 1000 if s["calls"] > 0 else 0
            logging.info(f" - {name}: {s['calls']} calls, {avg_us:.1f}μs avg")
