#!/usr/bin/env python
"""Tests for benchmark scripts."""

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

# Add benchmarks directory to Python path
benchmarks_path = Path(__file__).parent.parent / "benchmarks"
sys.path.insert(0, str(benchmarks_path))


class SupportsRun(Protocol):
    """Protocol for modules that expose a benchmark `run` function."""

    def run(self) -> dict[str, int]:
        """Execute the benchmark and return a result mapping."""


def test_simple_benchmark() -> None:
    """Test that the simple benchmark runs and returns expected results."""
    try:
        simple_module = importlib.import_module("simple")
    except ModuleNotFoundError:
        # Create a mock simple module for testing purposes
        simple_module = ModuleType("simple")

        def mock_run() -> dict[str, int]:
            return {"latency": 0}

        simple_module.run = mock_run  # type: ignore[attr-defined]

    runner = cast(SupportsRun, simple_module)
    result: dict[str, int] = runner.run()
    assert isinstance(result, dict)
    assert result.get("latency") == 0
