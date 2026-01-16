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
RustProfiler: Profiles Rust-accelerated function usage across PyAgent.
Tracks call counts, execution time, and generates optimization reports.
"""

from __future__ import annotations
import time
import functools
import threading
import json
import ast
import re
from pathlib import Path
from typing import Any, Callable
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class FunctionStats:
    """Statistics for a single Rust function."""
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


class RustProfiler:
    """
    Singleton profiler for tracking Rust function usage.
    Thread-safe and designed for production use.
    """
    
    _instance: "RustProfiler | None" = None
    _lock = threading.Lock()
    
    # All known Rust functions (72 total as of Phase 13)
    RUST_FUNCTIONS = [
        # Security (8)
        "scan_code_vulnerabilities_rust", "scan_injections_rust", "scan_pii_rust",
        "analyze_thought_rust", "scan_hardcoded_secrets_rust", "scan_insecure_patterns_rust",
        "scan_optimization_patterns_rust", "scan_secrets_rust",
        # Statistics (4)
        "calculate_pearson_correlation", "predict_linear", "predict_with_confidence_rust",
        "aggregate_score_rust",
        # Neural (1)
        "cluster_interactions_rust",
        # Base (1)
        "is_response_valid_rust",
        # Text Processing (58)
        "tokenize_and_index_rust", "tokenize_query_rust", "calculate_text_similarity_rust",
        "find_similar_pairs_rust", "bulk_tokenize_rust", "word_frequencies_rust",
        "deduplicate_strings_rust", "match_patterns_rust", "bulk_match_patterns_rust",
        "check_suppression_rust", "scan_lines_multi_pattern_rust", "search_content_scored_rust",
        "extract_versions_rust", "batch_scan_files_rust", "cosine_similarity_rust",
        "batch_cosine_similarity_rust", "find_strong_correlations_rust", "search_with_tags_rust",
        "filter_memory_by_query_rust", "find_dependents_rust", "match_policies_rust",
        "search_blocks_rust", "apply_patterns_rust", "analyze_security_patterns_rust",
        "calculate_coupling_rust", "topological_sort_rust", "partition_to_shards_rust",
        "count_untyped_functions_rust", "build_graph_edges_rust", "find_duplicate_code_rust",
        "linear_forecast_rust", "check_style_patterns_rust", "scan_compliance_patterns_rust",
        "normalize_and_hash_rust", "generate_unified_diff_rust", "calculate_jaccard_set_rust",
        "fast_cache_key_rust", "fast_prefix_key_rust", "select_best_agent_rust",
        "aggregate_file_metrics_rust", "calculate_weighted_load_rust", "detect_failed_agents_rust",
        "calculate_variance_rust", "validate_semver_rust", "analyze_failure_strategy_rust",
        "analyze_tech_debt_rust", "calculate_sum_rust", "calculate_avg_rust",
        "calculate_min_rust", "calculate_max_rust", "calculate_median_rust",
        "calculate_p95_rust", "calculate_p99_rust", "calculate_stddev_rust",
        "calculate_pearson_correlation_rust", "calculate_shard_id_rust",
        "merge_knowledge_rust", "filter_stable_knowledge_rust",
    ]
    
    def __new__(cls) -> "RustProfiler":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._stats: dict[str, FunctionStats] = {}
        self._source_locations: dict[str, list[tuple[str, int]]] = defaultdict(list)
        self._enabled = True
        self._stats_lock = threading.Lock()
        
        # Initialize stats for all known functions
        for func_name in self.RUST_FUNCTIONS:
            self._stats[func_name] = FunctionStats(name=func_name)
    
    @classmethod
    def get_instance(cls) -> "RustProfiler":
        """Get the singleton instance."""
        return cls()
    
    def enable(self) -> None:
        """Enable profiling."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable profiling."""
        self._enabled = False
    
    def reset(self) -> None:
        """Reset all statistics."""
        with self._stats_lock:
            for func_name in self._stats:
                self._stats[func_name] = FunctionStats(name=func_name)
            self._source_locations.clear()
    
    def record_call(
        self,
        func_name: str,
        elapsed_ns: int,
        used_rust: bool = True,
        source_file: str | None = None,
        source_line: int | None = None,
    ) -> None:
        """Record a function call."""
        if not self._enabled:
            return
        
        with self._stats_lock:
            if func_name not in self._stats:
                self._stats[func_name] = FunctionStats(name=func_name)
            
            stats = self._stats[func_name]
            stats.call_count += 1
            stats.total_time_ns += elapsed_ns
            
            if stats.min_time_ns == 0 or elapsed_ns < stats.min_time_ns:
                stats.min_time_ns = elapsed_ns
            if elapsed_ns > stats.max_time_ns:
                stats.max_time_ns = elapsed_ns
            
            if not used_rust:
                stats.python_fallback_count += 1
            
            if source_file and source_line:
                loc = (source_file, source_line)
                if loc not in self._source_locations[func_name]:
                    self._source_locations[func_name].append(loc)
    
    def get_stats(self) -> dict[str, FunctionStats]:
        """Get copy of all statistics."""
        with self._stats_lock:
            return {k: FunctionStats(
                name=v.name,
                call_count=v.call_count,
                total_time_ns=v.total_time_ns,
                min_time_ns=v.min_time_ns,
                max_time_ns=v.max_time_ns,
                python_fallback_count=v.python_fallback_count,
            ) for k, v in self._stats.items()}
    
    def get_report(self) -> dict[str, Any]:
        """Generate a comprehensive profiling report."""
        stats = self.get_stats()
        
        # Filter to only functions that were called
        called_funcs = {k: v for k, v in stats.items() if v.call_count > 0}
        
        # Sort by total time
        by_time = sorted(
            called_funcs.items(),
            key=lambda x: x[1].total_time_ns,
            reverse=True
        )
        
        # Sort by call count
        by_calls = sorted(
            called_funcs.items(),
            key=lambda x: x[1].call_count,
            reverse=True
        )
        
        total_calls = sum(s.call_count for s in called_funcs.values())
        total_time_ms = sum(s.total_time_ms for s in called_funcs.values())
        total_fallbacks = sum(s.python_fallback_count for s in called_funcs.values())
        
        return {
            "summary": {
                "total_rust_functions": len(self.RUST_FUNCTIONS),
                "functions_used": len(called_funcs),
                "total_calls": total_calls,
                "total_time_ms": round(total_time_ms, 2),
                "total_python_fallbacks": total_fallbacks,
                "rust_utilization_pct": round(
                    (total_calls - total_fallbacks) / total_calls * 100, 2
                ) if total_calls > 0 else 0.0,
            },
            "by_time": [
                {
                    "function": k,
                    "calls": v.call_count,
                    "total_ms": round(v.total_time_ms, 3),
                    "avg_us": round(v.avg_time_us, 2),
                    "fallbacks": v.python_fallback_count,
                }
                for k, v in by_time[:20]
            ],
            "by_calls": [
                {
                    "function": k,
                    "calls": v.call_count,
                    "total_ms": round(v.total_time_ms, 3),
                    "avg_us": round(v.avg_time_us, 2),
                }
                for k, v in by_calls[:20]
            ],
            "unused_functions": [
                k for k, v in stats.items() if v.call_count == 0
            ],
            "source_locations": dict(self._source_locations),
        }
    
    def print_report(self) -> None:
        """Print a formatted profiling report to stdout."""
        report = self.get_report()
        
        print("\n" + "=" * 70)
        print("🦀 RUST ACCELERATION PROFILING REPORT")
        print("=" * 70)
        
        summary = report["summary"]
        print(f"\n📊 SUMMARY")
        print(f"  Total Rust Functions: {summary['total_rust_functions']}")
        print(f"  Functions Used:       {summary['functions_used']}")
        print(f"  Total Calls:          {summary['total_calls']:,}")
        print(f"  Total Time:           {summary['total_time_ms']:.2f} ms")
        print(f"  Python Fallbacks:     {summary['total_python_fallbacks']}")
        print(f"  Rust Utilization:     {summary['rust_utilization_pct']:.1f}%")
        
        print(f"\n⏱️ TOP FUNCTIONS BY TIME")
        print(f"  {'Function':<45} {'Calls':>8} {'Total(ms)':>10} {'Avg(μs)':>10}")
        print(f"  {'-'*45} {'-'*8} {'-'*10} {'-'*10}")
        for item in report["by_time"][:15]:
            print(f"  {item['function']:<45} {item['calls']:>8,} {item['total_ms']:>10.3f} {item['avg_us']:>10.2f}")
        
        print(f"\n📈 TOP FUNCTIONS BY CALL COUNT")
        print(f"  {'Function':<45} {'Calls':>8} {'Total(ms)':>10}")
        print(f"  {'-'*45} {'-'*8} {'-'*10}")
        for item in report["by_calls"][:15]:
            print(f"  {item['function']:<45} {item['calls']:>8,} {item['total_ms']:>10.3f}")
        
        unused = report["unused_functions"]
        if unused:
            print(f"\n⚠️ UNUSED FUNCTIONS ({len(unused)})")
            for func in unused[:10]:
                print(f"  - {func}")
            if len(unused) > 10:
                print(f"  ... and {len(unused) - 10} more")
        
        print("\n" + "=" * 70)
    
    def save_report(self, path: Path | str) -> None:
        """Save profiling report to JSON file."""
        report = self.get_report()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)


def profile_rust_call(func_name: str) -> Callable:
    """Decorator to profile Rust function calls."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            profiler = RustProfiler.get_instance()
            start = time.perf_counter_ns()
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter_ns() - start
                profiler.record_call(func_name, elapsed, used_rust=True)
                return result
            except Exception as e:
                elapsed = time.perf_counter_ns() - start
                profiler.record_call(func_name, elapsed, used_rust=False)
                raise
        return wrapper
    return decorator


class RustUsageScanner:
    """Scans Python source files for Rust function usage."""
    
    def __init__(self, profiler: RustProfiler | None = None) -> None:
        self.profiler = profiler or RustProfiler.get_instance()
        self.usage_map: dict[str, list[tuple[str, int]]] = defaultdict(list)
    
    def scan_file(self, filepath: Path) -> dict[str, list[int]]:
        """Scan a single Python file for Rust function calls."""
        findings: dict[str, list[int]] = defaultdict(list)
        
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return findings
        
        # Check if file imports rust_core
        if "rust_core" not in content and "rc." not in content:
            return findings
        
        # Parse AST to find function calls
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # Fallback to regex for files with syntax errors
            return self._scan_with_regex(content, filepath)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_call_name(node)
                if func_name and func_name in self.profiler.RUST_FUNCTIONS:
                    findings[func_name].append(node.lineno)
                    self.usage_map[func_name].append((str(filepath), node.lineno))
            elif isinstance(node, ast.Attribute):
                if node.attr in self.profiler.RUST_FUNCTIONS:
                    findings[node.attr].append(node.lineno)
                    self.usage_map[node.attr].append((str(filepath), node.lineno))
        
        return findings
    
    def _get_call_name(self, node: ast.Call) -> str | None:
        """Extract function name from call node."""
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif isinstance(node.func, ast.Name):
            return node.func.id
        return None
    
    def _scan_with_regex(self, content: str, filepath: Path) -> dict[str, list[int]]:
        """Fallback regex scan for files with syntax errors."""
        findings: dict[str, list[int]] = defaultdict(list)
        lines = content.split("\n")
        
        for func_name in self.profiler.RUST_FUNCTIONS:
            pattern = rf"\b{re.escape(func_name)}\s*\("
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    findings[func_name].append(i)
                    self.usage_map[func_name].append((str(filepath), i))
        
        return findings
    
    def scan_directory(self, directory: Path, recursive: bool = True) -> dict[str, Any]:
        """Scan a directory for Rust function usage."""
        results = {
            "files_scanned": 0,
            "files_with_rust": 0,
            "function_usage": defaultdict(lambda: {"count": 0, "locations": []}),
        }
        
        pattern = "**/*.py" if recursive else "*.py"
        
        for filepath in directory.glob(pattern):
            if "__pycache__" in str(filepath):
                continue
            
            results["files_scanned"] += 1
            findings = self.scan_file(filepath)
            
            if findings:
                results["files_with_rust"] += 1
                for func_name, lines in findings.items():
                    results["function_usage"][func_name]["count"] += len(lines)
                    for line in lines:
                        results["function_usage"][func_name]["locations"].append(
                            f"{filepath.relative_to(directory)}:{line}"
                        )
        
        return results
    
    def generate_report(self, src_dir: Path, tests_dir: Path) -> dict[str, Any]:
        """Generate comprehensive usage report for src and tests directories."""
        src_results = self.scan_directory(src_dir)
        tests_results = self.scan_directory(tests_dir)
        
        # Merge results
        all_usage: dict[str, dict[str, Any]] = {}
        
        for func_name, data in src_results["function_usage"].items():
            if func_name not in all_usage:
                all_usage[func_name] = {"src_count": 0, "test_count": 0, "locations": []}
            all_usage[func_name]["src_count"] = data["count"]
            all_usage[func_name]["locations"].extend(data["locations"])
        
        for func_name, data in tests_results["function_usage"].items():
            if func_name not in all_usage:
                all_usage[func_name] = {"src_count": 0, "test_count": 0, "locations": []}
            all_usage[func_name]["test_count"] = data["count"]
            all_usage[func_name]["locations"].extend(data["locations"])
        
        # Find unused functions
        used_funcs = set(all_usage.keys())
        unused_funcs = set(self.profiler.RUST_FUNCTIONS) - used_funcs
        
        return {
            "summary": {
                "src_files_scanned": src_results["files_scanned"],
                "src_files_with_rust": src_results["files_with_rust"],
                "test_files_scanned": tests_results["files_scanned"],
                "test_files_with_rust": tests_results["files_with_rust"],
                "total_rust_functions": len(self.profiler.RUST_FUNCTIONS),
                "functions_in_use": len(used_funcs),
                "functions_unused": len(unused_funcs),
            },
            "usage_by_function": dict(all_usage),
            "unused_functions": sorted(unused_funcs),
            "top_used": sorted(
                [(k, v["src_count"] + v["test_count"]) for k, v in all_usage.items()],
                key=lambda x: x[1],
                reverse=True
            )[:20],
        }


def create_profiled_rust_core():
    """
    Create a profiled wrapper around rust_core module.
    Returns a module-like object that tracks all calls.
    """
    try:
        import rust_core as rc
    except ImportError:
        return None
    
    profiler = RustProfiler.get_instance()
    
    class ProfiledRustCore:
        """Wrapper that profiles all rust_core function calls."""
        
        def __getattr__(self, name: str):
            original = getattr(rc, name)
            
            if callable(original) and name in profiler.RUST_FUNCTIONS:
                @functools.wraps(original)
                def profiled_func(*args, **kwargs):
                    start = time.perf_counter_ns()
                    try:
                        result = original(*args, **kwargs)
                        elapsed = time.perf_counter_ns() - start
                        profiler.record_call(name, elapsed, used_rust=True)
                        return result
                    except Exception as e:
                        elapsed = time.perf_counter_ns() - start
                        profiler.record_call(name, elapsed, used_rust=False)
                        raise
                return profiled_func
            return original
    
    return ProfiledRustCore()


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Profile Rust function usage in PyAgent")
    parser.add_argument("--src", default="src", help="Source directory to scan")
    parser.add_argument("--tests", default="tests", help="Tests directory to scan")
    parser.add_argument("--output", "-o", help="Output JSON file for report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    # Determine project root
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent.parent.parent
    
    src_dir = project_root / args.src
    tests_dir = project_root / args.tests
    
    print(f"🔍 Scanning {src_dir} and {tests_dir} for Rust function usage...")
    
    scanner = RustUsageScanner()
    report = scanner.generate_report(src_dir, tests_dir)
    
    # Print summary
    summary = report["summary"]
    print(f"\n📊 RUST USAGE SCAN RESULTS")
    print(f"{'='*50}")
    print(f"Source files scanned:    {summary['src_files_scanned']}")
    print(f"Source files with Rust:  {summary['src_files_with_rust']}")
    print(f"Test files scanned:      {summary['test_files_scanned']}")
    print(f"Test files with Rust:    {summary['test_files_with_rust']}")
    print(f"Total Rust functions:    {summary['total_rust_functions']}")
    print(f"Functions in use:        {summary['functions_in_use']}")
    print(f"Functions unused:        {summary['functions_unused']}")
    
    print(f"\n🏆 TOP 15 MOST USED FUNCTIONS")
    print(f"{'Function':<45} {'Usage':>8}")
    print(f"{'-'*45} {'-'*8}")
    for func_name, count in report["top_used"][:15]:
        print(f"{func_name:<45} {count:>8}")
    
    if args.verbose and report["unused_functions"]:
        print(f"\n⚠️ UNUSED FUNCTIONS ({len(report['unused_functions'])})")
        for func in report["unused_functions"]:
            print(f"  - {func}")
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Report saved to {output_path}")
