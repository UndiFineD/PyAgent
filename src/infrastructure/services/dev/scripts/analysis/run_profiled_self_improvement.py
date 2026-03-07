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
from __future__ import annotations

import atexit
import cProfile
import functools
import json
import os
import sys
import time

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Ensure project root is in path FIRST
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

src_path = os.path.join(project_root, "src")

# Import from absolute module path
from src.infrastructure.services.dev.scripts.run_fleet_self_improvement import (
    main as run_self_improvement_main
)


# =============================================================================
# RUST PROFILER (Custom wrapper)
# =============================================================================
@dataclass
class RustFunctionStats:
    """Statistics for a Rust function."""

    name: str
    call_count: int = 0
    total_time_ns: int = 0

    @property
    def avg_time_us(self) -> float:
        """Average time per call in microseconds."""
        return (
            (self.total_time_ns / self.call_count / 1000.0)
            if self.call_count > 0
            else 0.0
        )

    @property
    def total_time_ms(self) -> float:
        """Total time in milliseconds."""
        return self.total_time_ns / 1_000_000.0


class RustProfiler:
    """Profiler specifically for rust_core function calls."""
    _instance = None
    _stats: dict[str, RustFunctionStats] = {}

    def __new__(cls) -> RustProfiler:
        """Singleton pattern to ensure one global profiler instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._stats = {}
        return cls._instance

    def record_call(self, func_name: str, elapsed_ns: int) -> None:
        """Record a call to a Rust function."""
        if func_name not in self._stats:
            self._stats[func_name] = RustFunctionStats(name=func_name)
        self._stats[func_name].call_count += 1
        self._stats[func_name].total_time_ns += elapsed_ns

    def get_stats(self) -> dict[str, RustFunctionStats]:
        """Get stats for all profiled Rust functions."""
        return {k: v for k, v in self._stats.items() if v.call_count > 0}


rust_profiler = RustProfiler()

# Wrap rust_core
try:
    import rust_core as _original_rc

    class ProfiledRustCore:
        """Wrapper that profiles all rust_core function calls."""

        def __getattr__(self, name: str) -> object:
            """Intercept attribute access to wrap callable functions for profiling."""
            original = getattr(_original_rc, name)

            if callable(original):

                @functools.wraps(original)
                def profiled_func(*args, **kwargs):
                    """Profile a call to a Rust function and record it in the RustProfiler."""
                    start_time_ns = time.perf_counter_ns()
                    try:
                        return original(*args, **kwargs)
                    finally:
                        elapsed_ns = time.perf_counter_ns() - start_time_ns
                        rust_profiler.record_call(name, elapsed_ns)

                return profiled_func
            return original

    sys.modules["rust_core"] = ProfiledRustCore()  # type: ignore[assignment]
    print("🦀 Rust profiling enabled")
except ImportError:
    print("⚠️ rust_core not available")


# =============================================================================
# COMPREHENSIVE PROFILE ANALYZER
# =============================================================================
class ComprehensiveProfileAnalyzer:
    """Analyzes cProfile results and filters for src/ code."""

    def __init__(self, src_dir: str, proj_root: str) -> None:
        """Initialize with src/ directory to focus on and project root for path normalization."""
        self._src_dir = src_dir
        self._proj_root = proj_root
        self.profiler = cProfile.Profile()
        self._start_time = None

    def start(self) -> None:
        """Start profiling."""
        self._start_time = time.time()
        self.profiler.enable()

    def stop(self) -> None:
        """Stop profiling."""
        self.profiler.disable()

    def _is_src_file(self, filename: str) -> bool:
        """Check if a file is in src/."""
        if not filename:
            return False
        # Normalize path for comparison
        try:
            norm_file = os.path.normpath(filename)
            norm_src = os.path.normpath(self._src_dir)
            return norm_file.startswith(norm_src)
        except (TypeError, AttributeError, ValueError):
            # Defensive: filename or src_path may be None or malformed
            return False

    def _clean_filename(self, filename: str) -> str:
        """Convert full path to relative module-style path."""
        try:
            rel = os.path.relpath(filename, self._proj_root)
            return rel.replace(os.sep, ".").replace(".py", "")
        except (ValueError, TypeError):
            # Defensive: filename/project_root may be malformed
            return filename

    def analyze(self) -> dict:
        """Analyze profiling results and return structured data."""
        # Extract raw stats
        raw_stats = (
            self.profiler.getstats()
        )  # List of profiler_entry tuples

        # Filter and process for src/ only
        src_functions = []
        module_stats: dict[str, dict[str, int | float | set[str]]] = defaultdict(
            lambda: {"call_count": 0, "total_time_s": 0.0, "functions": set()}
        )

        for entry in raw_stats:
            # Handle both code objects and string filenames
            if isinstance(entry.code, str):
                filename = entry.code
                func_name = "unknown"
            else:
                filename = entry.code.co_filename
                _line = entry.code.co_firstlineno
                func_name = entry.code.co_name
            (ncalls, totcalls, tottime, cumtime) = (
                entry.callcount,
                entry.callcount,
                entry.inlinetime,
                entry.totaltime,
            )
            if self._is_src_file(filename):
                module = self._clean_filename(filename)
                qualified_name = f"{module}.{func_name}"

                src_functions.append(
                    {
                        "function": qualified_name,
                        "ncalls": ncalls,
                        "totcalls": totcalls,
                        "tottime_s": tottime,
                        "cumtime_s": cumtime,
                        "tottime_ms": tottime * 1000,
                        "cumtime_ms": cumtime * 1000,
                        "avg_us": (tottime / ncalls * 1_000_000) if ncalls > 0 else 0,
                    }
                )

                # Safely extract and update call_count (always int)
                current_call_count = module_stats[module]["call_count"]
                assert isinstance(current_call_count, int)
                module_stats[module]["call_count"] = current_call_count + ncalls

                # Safely extract and update total_time_s (always float)
                current_total_time = module_stats[module]["total_time_s"]
                assert isinstance(current_total_time, float)
                module_stats[module]["total_time_s"] = current_total_time + tottime

                # Safely extract and update functions (always set)
                functions_set = module_stats[module]["functions"]
                assert isinstance(functions_set, set)
                functions_set.add(func_name)

        # Sort by cumulative time
        by_cumtime = sorted(src_functions, key=lambda x: x["cumtime_s"], reverse=True)
        by_tottime = sorted(src_functions, key=lambda x: x["tottime_s"], reverse=True)
        by_calls = sorted(src_functions, key=lambda x: x["ncalls"], reverse=True)

        # Module summary
        module_summary = sorted(
            [
                {
                    "module": k,
                    "call_count": v["call_count"],
                    "total_time_ms": float(v["total_time_s"]) * 1000 if isinstance(v["total_time_s"], (int, float)) else 0.0,
                    "function_count": len(v["functions"]) if isinstance(v["functions"], set) else 0,
                }
                for k, v in module_stats.items()
            ],
            key=lambda x: x["total_time_ms"],
            reverse=True,
        )

        # Get Rust stats
        rust_stats = rust_profiler.get_stats()
        rust_by_time = sorted(
            [
                {
                    "function": k,
                    "calls": v.call_count,
                    "total_ms": v.total_time_ms,
                    "avg_us": v.avg_time_us,
                }
                for k, v in rust_stats.items()
            ],
            key=lambda x: x["total_ms"],
            reverse=True,
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "python_functions_profiled": len(src_functions),
                "python_total_calls": sum(f["ncalls"] for f in src_functions),
                "python_total_time_ms": sum(f["tottime_ms"] for f in src_functions),
                "rust_functions_used": len(rust_stats),
                "rust_total_calls": sum(s.call_count for s in rust_stats.values()),
                "rust_total_time_ms": sum(s.total_time_ms for s in rust_stats.values()),
                "modules_profiled": len(module_stats),
            },
            "python_by_cumtime": by_cumtime[:50],
            "python_by_tottime": by_tottime[:50],
            "python_by_calls": by_calls[:50],
            "rust_by_time": rust_by_time[:30],
            "modules": module_summary[:30],
        }

    def print_report(self, report: dict) -> None:
        """Print formatted report."""
        summary = report["summary"]

        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE PROFILING REPORT")
        print("=" * 80)

        print(f"\n{'─' * 40}")
        print("📈 SUMMARY")
        print(f"{'─' * 40}")
        print(f"  Python Functions Profiled: {summary['python_functions_profiled']:,}")
        print(f"  Python Total Calls:        {summary['python_total_calls']:,}")
        print(f"  Python Total Time:         {summary['python_total_time_ms']:.2f} ms")
        print(f"  Rust Functions Used:       {summary['rust_functions_used']:,}")
        print(f"  Rust Total Calls:          {summary['rust_total_calls']:,}")
        print(f"  Rust Total Time:           {summary['rust_total_time_ms']:.2f} ms")
        print(f"  Modules Profiled:          {summary['modules_profiled']:,}")

        # Top by cumulative time (including child calls)
        if report["python_by_cumtime"]:
            print(f"\n{'─' * 40}")
            print("🐍 TOP PYTHON BY CUMULATIVE TIME (incl. child calls)")
            print(f"{'─' * 40}")
            print(f"  {'Function':<50} {'Calls':>8} {'Cum(ms)':>10} {'Own(ms)':>10}")
            print(f"  {'-' * 50} {'-' * 8} {'-' * 10} {'-' * 10}")
            for item in report["python_by_cumtime"][:20]:
                name = item["function"]
                if len(name) > 50:
                    name = "..." + name[-47:]
                print(
                    f"  {name:<50} {item['ncalls']:>8,} {item['cumtime_ms']:>10.2f} {item['tottime_ms']:>10.2f}"
                )

        # Top by own time (excluding child calls)
        if report["python_by_tottime"]:
            print(f"\n{'─' * 40}")
            print("⏱️ TOP PYTHON BY OWN TIME (excl. child calls)")
            print(f"{'─' * 40}")
            print(f"  {'Function':<50} {'Calls':>8} {'Own(ms)':>10} {'Avg(μs)':>10}")
            print(f"  {'-' * 50} {'-' * 8} {'-' * 10} {'-' * 10}")
            for item in report["python_by_tottime"][:15]:
                name = item["function"]
                if len(name) > 50:
                    name = "..." + name[-47:]
                print(
                    f"  {name:<50} {item['ncalls']:>8,} {item['tottime_ms']:>10.2f} {item['avg_us']:>10.1f}"
                )

        # Top by call count
        if report["python_by_calls"]:
            print(f"\n{'─' * 40}")
            print("📞 TOP PYTHON BY CALL COUNT")
            print(f"{'─' * 40}")
            print(f"  {'Function':<50} {'Calls':>10} {'Own(ms)':>10}")
            print(f"  {'-' * 50} {'-' * 10} {'-' * 10}")
            for item in report["python_by_calls"][:15]:
                name = item["function"]
                if len(name) > 50:
                    name = "..." + name[-47:]
                print(f"  {name:<50} {item['ncalls']:>10,} {item['tottime_ms']:>10.2f}")

        # Rust functions
        if report["rust_by_time"]:
            print(f"\n{'─' * 40}")
            print("🦀 RUST FUNCTIONS BY TIME")
            print(f"{'─' * 40}")
            print(f"  {'Function':<45} {'Calls':>8} {'Total(ms)':>10} {'Avg(μs)':>10}")
            print(f"  {'-' * 45} {'-' * 8} {'-' * 10} {'-' * 10}")
            for item in report["rust_by_time"][:15]:
                print(
                    f"  {item['function']:<45} {item['calls']:>8,} "
                    f"{item['total_ms']:>10.3f} {item['avg_us']:>10.2f}"
                )

        # Modules
        if report["modules"]:
            print(f"\n{'─' * 40}")
            print("📦 TOP MODULES BY TIME")
            print(f"{'─' * 40}")
            print(f"  {'Module':<45} {'Calls':>10} {'Time(ms)':>10} {'Funcs':>6}")
            print(f"  {'-' * 45} {'-' * 10} {'-' * 10} {'-' * 6}")
            for item in report["modules"][:15]:
                mod = item["module"]
                if len(mod) > 45:
                    mod = "..." + mod[-42:]
                print(
                    f"  {mod:<45} {item['call_count']:>10,} {item['total_time_ms']:>10.2f} {item['function_count']:>6}"
                )

        print("\n" + "=" * 80)


# =============================================================================
# MAIN
# =============================================================================
print("🐍 Python profiling enabled - using cProfile for src/ code")
# Initialize analyzer
analyzer = ComprehensiveProfileAnalyzer(src_path, project_root)


def save_profile_report() -> None:
    """Save profiling report on exit."""
    analyzer.stop()
    report = analyzer.analyze()

    # Create reports directory
    reports_dir = Path(project_root) / "data" / "logs" / "profiles"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"comprehensive_profile_{timestamp}.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Print report
    analyzer.print_report(report)
    print(f"\n💾 Detailed report saved to: {report_path}")


# Register cleanup
atexit.register(save_profile_report)


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 COMPREHENSIVE PROFILED SELF IMPROVEMENT")
    print("=" * 60)
    print(f"Start time: {datetime.now().isoformat()}")
    print(f"Profiling: All functions in {src_path}")
    print()

    start_time = time.time()

    # Start profiling
    analyzer.start()

    try:
        run_self_improvement_main()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        # Broad except is justified here to ensure all errors are logged and surfaced in profiling context
        print(f"\n❌ Error: {e}")
        raise
    finally:
        elapsed_time = time.time() - start_time
        print(f"\n⏱️ Total execution time: {elapsed_time:.2f} seconds")
