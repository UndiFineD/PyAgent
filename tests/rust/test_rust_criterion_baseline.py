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
"""Red-phase contracts for Rust Criterion baseline benchmark wiring."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path


def _repo_root() -> Path:
    """Return repository root based on this file location.

    Returns:
        Path: Absolute path to repository root.

    """
    return Path(__file__).resolve().parents[2]


def _load_rust_core_cargo() -> dict:
    """Load and parse rust_core/Cargo.toml.

    Returns:
        dict: Parsed TOML mapping.

    """
    cargo_path = _repo_root() / "rust_core" / "Cargo.toml"
    with cargo_path.open("rb") as fh:
        return tomllib.load(fh)


def _stats_benchmark_source() -> str:
    """Read rust_core benchmark source for stats baseline harness.

    Returns:
        str: UTF-8 text for stats_baseline benchmark source.

    """
    bench_path = _repo_root() / "rust_core" / "benches" / "stats_baseline.rs"
    return bench_path.read_text(encoding="utf-8")


def test_rust_core_cargo_declares_criterion_baseline_bench_contract() -> None:
    """Cargo config must declare Criterion and stats_baseline bench target.

    This asserts IFACE-BENCH-001 contract markers in `rust_core/Cargo.toml`.
    It intentionally fails in red phase until Criterion wiring is implemented.

    """
    cargo = _load_rust_core_cargo()

    dev_dependencies = cargo.get("dev-dependencies", {})
    assert "criterion" in dev_dependencies, (
        "rust_core/Cargo.toml must add criterion under [dev-dependencies] for stats baseline bench"
    )

    bench_entries = cargo.get("bench", [])
    assert isinstance(bench_entries, list), "Cargo bench target declarations must be a list"

    stats_baseline_entry = next(
        (entry for entry in bench_entries if isinstance(entry, dict) and entry.get("name") == "stats_baseline"),
        None,
    )
    assert stats_baseline_entry is not None, "rust_core/Cargo.toml must declare [[bench]] name='stats_baseline'"
    assert stats_baseline_entry.get("harness") is False, (
        "rust_core/Cargo.toml bench target 'stats_baseline' must set harness=false for Criterion"
    )


def test_stats_baseline_benchmark_file_uses_criterion_harness_patterns() -> None:
    """Benchmark source must exist and include Criterion harness macros.

    This fails in red phase if benchmark source or Criterion macros are absent.

    """
    bench_path = _repo_root() / "rust_core" / "benches" / "stats_baseline.rs"
    assert bench_path.is_file(), "rust_core/benches/stats_baseline.rs must exist"

    source = _stats_benchmark_source()
    assert "criterion_group!" in source, "stats_baseline benchmark must declare criterion_group!"
    assert "criterion_main!" in source, "stats_baseline benchmark must declare criterion_main!"
    assert "Criterion" in source, "stats_baseline benchmark must import/use Criterion type"


def test_stats_baseline_benchmark_contains_design_naming_contract_markers() -> None:
    """Benchmark source must encode stats group and benchmark-id naming contracts.

    Naming contract asserted here:
    1. Group name pattern: `stats/<domain>`.
    2. Benchmark ID pattern: `<function>/<dataset>`.

    """
    bench_path = _repo_root() / "rust_core" / "benches" / "stats_baseline.rs"
    assert bench_path.is_file(), "rust_core/benches/stats_baseline.rs must exist"

    source = _stats_benchmark_source()

    assert re.search(r"benchmark_group\(\s*\"stats/[a-zA-Z0-9_\-]+\"\s*\)", source) is not None, (
        "stats_baseline benchmark must define a group name matching stats/<domain>"
    )

    assert (
        re.search(r"BenchmarkId::new\(\s*\"[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+\"", source) is not None
        or re.search(r"bench_function\(\s*\"[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+\"", source) is not None
    ), "stats_baseline benchmark must define benchmark IDs matching <function>/<dataset>"
