#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
"""
Performance Profiling Suite for PyAgent.
Validates Rust-accelerated logic and monitors tokenization throughput.
"""

import sys
import asyncio
from pathlib import Path

# Robustly find the repository root by looking for the src directory
current_path = Path(__file__).resolve()
project_root = current_path
while project_root.name != 'src' and project_root.parent != project_root:
    project_root = project_root.parent
if project_root.name == 'src':
    project_root = project_root.parent

# DON'T add project_root to sys.path[0] immediately, or it will shadow rust_core folder
# sys.path.insert(0, str(project_root))

# Remove current directory from path to avoid shadowing rust_core with the folder
CURRENT_WORKING_DIR = str(Path.cwd())
print(f"DEBUG: Before cleaning sys.path: {sys.path[:3]}")
while CURRENT_WORKING_DIR in sys.path:
    sys.path.remove(CURRENT_WORKING_DIR)
while "" in sys.path:
    sys.path.remove("")
print(f"DEBUG: After cleaning sys.path: {sys.path[:3]}")

try:
    # Force profile rust_core BEFORE other imports
    import rust_core
    print(f"DEBUG: rust_core file: {getattr(rust_core, '__file__', 'None')}")

    # Now we can add project_root for other imports
    sys.path.insert(0, str(project_root))

    # pylint: disable=wrong-import-position
    from src.observability.profiling.rust_profiler import RustProfiler, create_profiled_rust_core
    print(f"DEBUG: rust_core dir count: {len(dir(rust_core))}")

    profiled_rc = create_profiled_rust_core()
    if profiled_rc:
        sys.modules['rust_core'] = profiled_rc
        print("DEBUG: sys.modules['rust_core'] patched")
except ImportError as e:
    print(f"DEBUG: Initial import error: {e}")

# pylint: disable=wrong-import-position
from src.infrastructure.services.benchmarks.benchmark_suite import BenchmarkSuite

async def main():
    """Main execution point for the profiling suite."""
    profiler = RustProfiler.get_instance()
    profiler.enable()

    # Verify that calling it manually works
    # pylint: disable=import-outside-toplevel
    import rust_core as rc
    print("DEBUG: Calling estimate_tokens_rust...")
    try:
        rc.estimate_tokens_rust("test")
    except (AttributeError, RuntimeError) as e:
        print(f"DEBUG: Manual call failed: {e}")

    stats = profiler.get_stats()
    print(f"DEBUG: Profiler calls for estimate_tokens_rust: {stats.get('estimate_tokens_rust')}")

    suite = BenchmarkSuite()

    # 1. Tokenization Benchmarks
    test_texts = {
        "Short": "What is Python?",
        "Medium": "Explain the concept of technical debt in software development.",
        "Long": (
            "Provide a comprehensive analysis of microservices architecture." * 50
        ),
        "Code": """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1
"""
    }

    print("\n🚀 Running Profiled Benchmarks...")
    suite.benchmark_tokenization(test_texts, iterations=1000)

    # 2. Sustained Throughput
    print("\n🚀 Running Sustained Throughput Test (5s)...")
    texts_list = list(test_texts.values())
    suite.run_sustained_throughput(texts_list, duration_seconds=5)

    # Print summaries
    suite.print_summary()
    profiler.print_report()

    # Save report
    report_path = project_root / "temp" / "profiling_report.json"
    profiler.save_report(report_path)
    print(f"\n✅ Dynamic profiling report saved to {report_path}")

if __name__ == "__main__":
    asyncio.run(main())
