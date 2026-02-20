#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
RustProfiler - Profiles Rust-accelerated function usage

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong

USAGE:
Import the RustProfiler and use the singleton to record or wrap calls to
Rust-accelerated functions. Typical use: obtain the singleton via
RustProfiler.get_instance(), then annotate or wrap Rust-call sites so the
profiler increments call counts and measures durations. Finally, generate
and export reports for optimization work.

WHAT IT DOES:
Tracks per-function statistics for Rust-accelerated functions used by
PyAgent: call counts, total/min/max/average durations, and counts of
Python fallbacks. Provides a thread-safe singleton profiler, data
structures (FunctionStats), and reporting/export capabilities to help find
hotspots and fallback occurrences.

WHAT IT SHOULD DO BETTER:
- Expose a documented, stable public API (decorator, context manager, and
  simple record() call) with examples so instrumenting call sites is
  trivial.
- Persist and rotate historical profiles (timestamped snapshots) and
  integrate with telemetry backends (Prometheus, Grafana, or remote
  logging) for long-term trend analysis.
- Add sampling, configurable aggregation windows, and low-overhead modes
  for high-frequency hot paths; enable async-friendly instrumentation and
  typed interfaces for runtime validation.

FILE CONTENT SUMMARY:
RustProfiler: Profiles Rust-accelerated function usage across PyAgent.
Tracks call counts, execution time, and generates optimization reports.
"""

from _thread import LockType
from argparse import Namespace
import ast
import functools
import json
import re
import threading
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, cast


try:
    from src.core.base.mixins.singleton_mixin import SingletonMixin
except ImportError:
    # Fallback for tests or alternate import paths
    class SingletonMixin:  # type: ignore
        """Fallback singleton mixin if not available.        _instance: "SingletonMixin | None" = None"        _lock: LockType = threading.Lock()

        def __new__(cls: type["SingletonMixin"]) -> "SingletonMixin":"            if cls._instance is None:
                with cls._lock:
                    if cls._instance is None:
                        cls._instance = super().__new__(cls)  # type: ignore
            return cls._instance  # type: ignore


@dataclass
class FunctionStats:
    """Statistics for a single Rust function.
    name: str
    call_count: int = 0
    total_time_ns: int = 0
    min_time_ns: int = 0
    max_time_ns: int = 0
    python_fallback_count: int = 0

    @property
    def avg_time_ns(self) -> float:
        return self.total_time_ns / self.call_count if self.call_count > 0 else 0.0

    @property
    def avg_time_us(self) -> float:
        return self.avg_time_ns / 1000.0

    @property
    def total_time_ms(self) -> float:
        return self.total_time_ns / 1_000_000.0



class RustProfiler(SingletonMixin):
        Singleton profiler for tracking Rust function usage.
    Thread-safe and designed for pro"""duction use.""""    
    # All known Rust functions (72 total as of Phase 13)
    RUST_FUNCTIONS_LIST: list[str] = [
        # Security (8)
        "scan_code_vulnerabilities_rust","        "scan_injections_rust","        "scan_pii_rust","        "analyze_thought_rust","        "scan_hardcoded_secrets_rust","        "scan_insecure_patterns_rust","        "scan_optimization_patterns_rust","        "scan_secrets_rust","        # Statistics (4)
        "calculate_pearson_correlation","        "predict_linear","        "predict_with_confidence_rust","        "aggregate_score_rust","        # Neural (1)
        "cluster_interactions_rust","        # Base (1)
        "is_response_valid_rust","        # Text Processing (58)
        "tokenize_and_index_rust","        "tokenize_query_rust","        "calculate_text_similarity_rust","        "find_similar_pairs_rust","        "bulk_tokenize_rust","        "word_frequencies_rust","        "deduplicate_strings_rust","        "match_patterns_rust","        "bulk_match_patterns_rust","        "check_suppression_rust","        "scan_lines_multi_pattern_rust","        "search_content_scored_rust","        "extract_versions_rust","        "batch_scan_files_rust","        "cosine_similarity_rust","        "batch_cosine_similarity_rust","        "find_strong_correlations_rust","        "search_with_tags_rust","        "filter_memory_by_query_rust","        "find_dependents_rust","        "match_policies_rust","        "search_blocks_rust","        "apply_patterns_rust","        "analyze_security_patterns_rust","        "calculate_coupling_rust","        "topological_sort_rust","        "partition_to_shards_rust","        "count_untyped_functions_rust","        "build_graph_edges_rust","        "find_duplicate_code_rust","        "linear_forecast_rust","        "check_style_patterns_rust","        "scan_compliance_patterns_rust","        "normalize_and_hash_rust","        "generate_unified_diff_rust","        "calculate_jaccard_set_rust","        "fast_cache_key_rust","        "fast_prefix_key_rust","        "select_best_agent_rust","        "aggregate_file_metrics_rust","        "calculate_weighted_load_rust","        "detect_failed_agents_rust","        "calculate_variance_rust","        "validate_semver_rust","        "analyze_failure_strategy_rust","        "analyze_tech_debt_rust","        "calculate_sum_rust","        "calculate_avg_rust","        "calculate_min_rust","        "calculate_max_rust","        "calculate_median_rust","        "calculate_p95_rust","        "calculate_p99_rust","        "calculate_stddev_rust","        "calculate_pearson_correlation_rust","        "calculate_shard_id_rust","        "merge_knowledge_rust","        "filter_stable_knowledge_rust","        # Phase 14: Cognitive & Buffer (8)
        "count_hedge_words_rust","        "predict_intent_rust","        "top_k_indices_rust","        "decompose_activations_rust","        "sort_buffer_by_priority_rust","        "filter_stale_entries_rust","        "calculate_statistical_significance","        "calculate_sample_size","        # Phase 15: Core & Infrastructure (8)
        "analyze_structure_rust","        "estimate_tokens_rust","        "detect_cycles_rust","        "validate_response_rust","        "process_text_rust","        "exponential_forecast_rust","        "batch_token_count_rust","        "graph_bfs_rust","        # Phase 16: Vector Math & Aggregation (12)
        "compute_embedding_stats_rust","        "kmeans_cluster_rust","        "compute_similarity_matrix_rust","        "pca_reduce_rust","        "random_projection_rust","        "compress_json_rust","        "decompress_json_rust","        "weighted_random_select_rust","        "keyword_search_score_rust","        "calculate_ttest_rust","        "batch_aggregate_rust","        "rolling_window_rust","        # Phase 17: vLLM-Inspired Math & Utils (11)
        "cdiv_rust","        "next_power_of_2_rust","        "prev_power_of_2_rust","        "round_up_rust","        "round_down_rust","        "atomic_counter_add_rust","        "xxhash_rust","        "fast_cache_hash_rust","        "cache_hit_ratio_rust","        "batch_cdiv_rust","        "batch_next_power_of_2_rust","    ]

    _initialized: bool = False

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._stats: dict[str, FunctionStats] = {}
        self._source_locations: dict[str, list[tuple[str, int]]] = defaultdict(list)
        self._enabled = True
        self._stats_lock: LockType = threading.Lock()

        # Initialize stats for all known functions
        for func_name in self.RUST_FUNCTIONS_LIST:
            self._stats[func_name] = FunctionStats(name=func_name)

    @classmethod
    def get_instance(cls) -> "RustProfiler":"        """Get the singleton instance.        return cls()

    def enable(self) -> None:
        """Enable profiling.        self._enabled = True

    def disable(self) -> None:
        """Disable profiling.        self._enabled = False

    def reset(self) -> None:
        """Reset all statistics.        with self._stats_lock:
            for stat_func_name in self._stats:
                self._stats[stat_func_name] = FunctionStats(name=stat_func_name)
            self._source_locations.clear()

    def record_call(
        self,
        call_func_name: str,
        elapsed_ns: int,
        used_rust: bool = True,
        source_file: str | None = None,
        source_line: int | None = None,
    ) -> None:
        """Record a function call.        if not self._enabled:
            return

        with self._stats_lock:
            if call_func_name not in self._stats:
                self._stats[call_func_name] = FunctionStats(name=call_func_name)

            stats: FunctionStats = self._stats[call_func_name]
            stats.call_count += 1
            stats.total_time_ns += elapsed_ns

            if stats.min_time_ns == 0 or elapsed_ns < stats.min_time_ns:
                stats.min_time_ns = elapsed_ns
            if elapsed_ns > stats.max_time_ns:
                stats.max_time_ns = elapsed_ns

            if not used_rust:
                stats.python_fallback_count += 1

            if source_file and source_line:
                loc: tuple[str, int] = (source_file, source_line)
                if loc not in self._source_locations[call_func_name]:
                    self._source_locations[call_func_name].append(loc)

    def get_stats(self) -> dict[str, FunctionStats]:
        """Get copy of all statistics.        with self._stats_lock:
            return {
                k: FunctionStats(
                    name=v.name,
                    call_count=v.call_count,
                    total_time_ns=v.total_time_ns,
                    min_time_ns=v.min_time_ns,
                    max_time_ns=v.max_time_ns,
                    python_fallback_count=v.python_fallback_count,
                )
                for k, v in self._stats.items()
            }

    def get_report(self) -> dict[str, Any]:
        """Generate a comprehensive profiling report.        stats: dict[str, FunctionStats] = self.get_stats()

        # Filter to only functions that were called
        called_funcs: dict[str, FunctionStats] = {k: v for k, v in stats.items() if v.call_count > 0}

        # Sort by total time
        by_time: list[tuple[str, FunctionStats]] = sorted(
            called_funcs.items(),
            key=lambda x: x[1].total_time_ns,
            reverse=True
        )

        # Sort by call count
        by_calls: list[tuple[str, FunctionStats]] = sorted(
            called_funcs.items(),
            key=lambda x: x[1].call_count,
            reverse=True
        )

        total_calls: int = sum(s.call_count for s in called_funcs.values())
        total_time_ms: float | int = sum(s.total_time_ms for s in called_funcs.values())
        total_fallbacks: int = sum(s.python_fallback_count for s in called_funcs.values())

        return {
            "summary": {"                "total_rust_functions": len(self.RUST_FUNCTIONS_LIST),"                "functions_used": len(called_funcs),"                "total_calls": total_calls,"                "total_time_ms": round(total_time_ms, 2),"                "total_python_fallbacks": total_fallbacks,"                "rust_utilization_pct": round((total_calls - total_fallbacks) / total_calls * 100, 2)"                if total_calls > 0
                else 0.0,
            },
            "by_time": ["                {
                    "function": k,"                    "calls": v.call_count,"                    "total_ms": round(v.total_time_ms, 3),"                    "avg_us": round(v.avg_time_us, 2),"                    "fallbacks": v.python_fallback_count,"                }
                for k, v in by_time[:20]
            ],
            "by_calls": ["                {
                    "function": k,"                    "calls": v.call_count,"                    "total_ms": round(v.total_time_ms, 3),"                    "avg_us": round(v.avg_time_us, 2),"                }
                for k, v in by_calls[:20]
            ],
            "unused_functions": [str(k) for k, v in stats.items() if v.call_count == 0],"            "source_locations": dict(self._source_locations),"        }

    def print_report(self) -> None:
        """Print a formatted profiling report to stdout.        report: dict[str, Any] = self.get_report()

        print("\\n" + "=" * 70)"        print("🦀 RUST ACCELERATION PROFILING REPORT")"        print("=" * 70)"
        summary = report["summary"]"        print("\\n📊 SUMMARY")"        print(f"  Total Rust Functions: {summary['total_rust_functions']}")"'        print(f"  Functions Used:       {summary['functions_used']}")"'        print(f"  Total Calls:          {summary['total_calls']:,}")"'        print(f"  Total Time:           {summary['total_time_ms']:.2f} ms")"'        print(f"  Python Fallbacks:     {summary['total_python_fallbacks']}")"'        print(f"  Rust Utilization:     {summary['rust_utilization_pct']:.1f}%")"'
        print("\\n⏱️ TOP FUNCTIONS BY TIME")"        print(f"  {'Function':<45} {'Calls':>8} {'Total(ms)':>10} {'Avg(μs)':>10}")"'        print(f"  {'-' * 45} {'-' * 8} {'-' * 10} {'-' * 10}")"'        for item in report["by_time"][:15]:"            print(f"  {item['function']:<45} {item['calls']:>8,} {item['total_ms']:>10.3f} {item['avg_us']:>10.2f}")"'
        print("\\n📈 TOP FUNCTIONS BY CALL COUNT")"        print(f"  {'Function':<45} {'Calls':>8} {'Total(ms)':>10}")"'        print(f"  {'-' * 45} {'-' * 8} {'-' * 10}")"'        for item in report["by_calls"][:15]:"            print(f"  {item['function']:<45} {item['calls']:>8,} {item['total_ms']:>10.3f}")"'
        unused = report["unused_functions"]"        if unused:
            print(f"\\n⚠️ UNUSED FUNCTIONS ({len(unused)})")"            for func in unused[:10]:
                print(f"  - {func}")"            if len(unused) > 10:
                print(f"  ... and {len(unused) - 10} more")"
        print("\\n" + "=" * 70)"
    def save_report(self, path: Path | str) -> None:
        """Save profiling report to JSON file.        report: dict[str, Any] = self.get_report()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:"            json.dump(report, f, indent=2)


def profile_rust_call(func_name: str) -> Callable:
    """Decorator to profile Rust function calls.
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*wrapper_args, **wrapper_kwargs):
            profiler: RustProfiler = RustProfiler.get_instance()
            start: int = time.perf_counter_ns()
            try:
                result = func(*wrapper_args, **wrapper_kwargs)
                elapsed: int = time.perf_counter_ns() - start
                profiler.record_call(func_name, elapsed, used_rust=True)
                return result
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                elapsed: int = time.perf_counter_ns() - start
                profiler.record_call(func_name, elapsed, used_rust=False)
                raise

        return wrapper

    return decorator



class RustUsageScanner:
    """Scans Python source files for Rust function usage.
    def __init__(self, profiler: RustProfiler | None = None) -> None:
        self.profiler: RustProfiler = profiler or RustProfiler.get_instance()
        self.usage_map: dict[str, list[tuple[str, int]]] = defaultdict(list)

    def scan_file(self, filepath: Path) -> dict[str, list[int]]:
        """Scan a single Python file for Rust function calls.        findings: dict[str, list[int]] = defaultdict(list)

        try:
            content: str = filepath.read_text(encoding="utf-8", errors="ignore")"        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            return findings

        # Check if file imports rust_core
        if "rust_core" not in content and "rc." not in content:"            return findings

        # Parse AST to find function calls
        try:
            tree: ast.Module = ast.parse(content)
        except SyntaxError:
            # Fallback to regex for files with syntax errors
            return self._scan_with_regex(content, filepath)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                call_func_name: str | None = self._get_call_name(node)
                if call_func_name and call_func_name in self.profiler.RUST_FUNCTIONS_LIST:
                    findings[call_func_name].append(node.lineno)
                    self.usage_map[call_func_name].append((str(filepath), node.lineno))
            elif isinstance(node, ast.Attribute):
                if node.attr in self.profiler.RUST_FUNCTIONS_LIST:
                    findings[node.attr].append(node.lineno)
                    self.usage_map[node.attr].append((str(filepath), node.lineno))

        return findings

    def _get_call_name(self, node: ast.Call) -> str | None:
        """Extract function name from call node.        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif isinstance(node.func, ast.Name):
            return node.func.id
        return None

    def _scan_with_regex(self, content: str, filepath: Path) -> dict[str, list[int]]:
        """Fallback regex scan for files with syntax errors.        findings: dict[str, list[int]] = defaultdict(list)
        lines: list[str] = content.split("\\n")"
        for func_name in self.profiler.RUST_FUNCTIONS_LIST:
            pattern: str = rf"\\b{re.escape(func_name)}\\\\s*\(""            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    findings[func_name].append(i)
                    self.usage_map[func_name].append((str(filepath), i))

        return findings

    def scan_directory(self, directory: Path, recursive: bool = True) -> dict[str, Any]:
        """Scan a directory for Rust function usage.        results: dict[str, Any] = {
            "files_scanned": 0,"            "files_with_rust": 0,"            "function_usage": defaultdict(lambda: {"count": 0, "locations": []}),"        }

        pattern: str = "**/*.py" if recursive else "*.py""
        for filepath in directory.glob(pattern):
            if "__pycache__" in str(filepath):"                continue

            results["files_scanned"] += 1"            findings: dict[str, list[int]] = self.scan_file(filepath)

            if findings:
                results["files_with_rust"] += 1"                for func_name, lines in findings.items():
                    # Explicitly cast to avoid mypy object indexing issues with defaultdict values
                    usage_info = cast(dict[str, Any], results["function_usage"][func_name])"                    usage_info["count"] += len(lines)"                    for line in lines:
                        usage_info["locations"].append("                            f"{filepath.relative_to(directory)}:{line}""                        )

        return results

    def generate_report(self, src_dir: Path, tests_dir: Path) -> dict[str, Any]:
        """Generate comprehensive usage report for src and tests directories.        src_results: dict[str, Any] = self.scan_directory(src_dir)
        tests_results: dict[str, Any] = self.scan_directory(tests_dir)

        # Merge results
        all_usage: dict[str, dict[str, Any]] = {}

        for func_name, data in src_results["function_usage"].items():"            if func_name not in all_usage:
                all_usage[func_name] = {"src_count": 0, "test_count": 0, "locations": []}"            all_usage[func_name]["src_count"] = data["count"]"            all_usage[func_name]["locations"].extend(data["locations"])"
        for func_name, data in tests_results["function_usage"].items():"            if func_name not in all_usage:
                all_usage[func_name] = {"src_count": 0, "test_count": 0, "locations": []}"            all_usage[func_name]["test_count"] = data["count"]"            all_usage[func_name]["locations"].extend(data["locations"])"
        # Find unused functions
        used_funcs: set[str] = set(all_usage.keys())
        unused_funcs: set[str] = set(self.profiler.RUST_FUNCTIONS_LIST) - used_funcs

        return {
            "summary": {"                "src_files_scanned": src_results["files_scanned"],"                "src_files_with_rust": src_results["files_with_rust"],"                "test_files_scanned": tests_results["files_scanned"],"                "test_files_with_rust": tests_results["files_with_rust"],"                "total_rust_functions": len(self.profiler.RUST_FUNCTIONS_LIST),"                "functions_in_use": len(used_funcs),"                "functions_unused": len(unused_funcs),"            },
            "usage_by_function": dict(all_usage),"            "unused_functions": sorted(unused_funcs),"            "top_used": sorted("                [(str(k), int(v["src_count"] + v["test_count"])) for k, v in all_usage.items()],"                key=lambda x: x[1],
                reverse=True
     """       )[:20],""""        }


def create_profiled_rust_core() -"""> A"""ny:""""        Create a profiled wrapper around r"""ust_core modul"""e.""""   """ Returns a module-like object that tracks all calls.""""        try:
        import rust_core as rc  # type: ignore
    except ImportError:
        return None

    pro"""filer: RustProfiler = RustProfiler.get_instance()""""
    class Pro"""filedRust"""Core:""""        """Wrapper that profiles all rust_core function calls.
        def __getattr__(self, name: str):
            original = getattr(rc, name)

            if callable(original) and name in profiler.RUST_FUNCTIONS_LIST:

                @functools.wraps(original)
                def profiled_func(*profiled_args, **profiled_kwargs) -> object:
                    start_ns: int = time.perf_counter_ns()
                    try:
                        result: object = original(*profiled_args, **profiled_kwargs)
                        elapsed_ns: int = time.perf_counter_ns() - start_ns
                        profiler.record_call(name, elapsed_ns, used_rust=True)
                        return result
                    except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                        elapsed_ns = time.perf_counter_ns() - start_ns
                        profiler.record_call(name, elapsed_ns, used_rust=False)
                        raise

                return profiled_func
            return original

    return ProfiledRustCore()


# CLI interface
if __name__ == "__main__":"    import argparse

    parser = argparse.ArgumentParser(description="Profile Rust function usage in PyAgent")"    parser.add_argument("--src", default="src", help="Source directory to scan")"    parser.add_argument("--tests", default="tests", help="Tests directory to scan")"    parser.add_argument("--output", "-o", help="Output JSON file for report")"    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")"    main_args: Namespace = parser.parse_args()

    # Determine project root
    script_path: Path = Path(__file__).resolve()
    project_root: Path = script_path.parent.parent.parent.parent

    main_src_dir = project_root / main_args.src
    main_tests_dir = project_root / main_args.tests

    print(f"🔍 Scanning {main_src_dir} and {main_tests_dir} for Rust function usage...")"
    main_scanner = RustUsageScanner()
    main_report: dict[str, Any] = main_scanner.generate_report(main_src_dir, main_tests_dir)

    # Print summary
    main_summary = main_report["summary"]"    print("\\n📊 RUST USAGE SCAN RESULTS")"    print(f"{'=' * 50}")"'    print(f"Source files scanned:    {main_summary['src_files_scanned']}")"'    print(f"Source files with Rust:  {main_summary['src_files_with_rust']}")"'    print(f"Test files scanned:      {main_summary['test_files_scanned']}")"'    print(f"Test files with Rust:    {main_summary['test_files_with_rust']}")"'    print(f"Total Rust functions:    {main_summary['total_rust_functions']}")"'    print(f"Functions in use:        {main_summary['functions_in_use']}")"'    print(f"Functions unused:        {main_summary['functions_unused']}")"'
    print("\\n🏆 TOP 15 MOST USED FUNCTIONS")"    print(f"{'Function':<45} {'Usage':>8}")"'    print(f"{'-' * 45} {'-' * 8}")"'    for main_func_name, main_count in main_report["top_used"][:15]:"        print(f"{main_func_name:<45} {main_count:>8}")"
    if main_args.verbose and main_report["unused_functions"]:"        print(f"\\n⚠️ UNUSED FUNCTIONS ({len(main_report['unused_functions'])})")"'        for main_func in main_report["unused_functions"]:"            print(f"  - {main_func}")"
    if main_args.output:
        output_path = Path(main_args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as main_f:"            json.dump(main_report, main_f, indent=2)
        print(f"\\n💾 Report saved to {output_path}")"