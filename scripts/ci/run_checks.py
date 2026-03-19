#!/usr/bin/env python3
"""Run a shared set of repository checks.

This script is intended to be used by both:
- pre-commit (local developer feedback)
- GitHub Actions (CI enforcement)

By default, it runs the "precommit" profile which is fast enough to run locally
on each commit but still catches most issues. The "ci" profile runs the full
suite used on GitHub.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


# Full CI test list (matches ci-python-core workflow)
CORE_TEST_FILES = [
    "tests/test_core_agent_state_manager.py",
    "tests/test_core_agent_registry.py",
    "tests/test_core_helpers.py",
    "tests/test_core_observability.py",
    "tests/test_core_quality.py",
    "tests/test_core_runtime.py",
    "tests/test_core_task_queue.py",
    "tests/test_core_workflow_engine.py",
    "tests/test_workflow_engine.py",
    "tests/test_task.py",
    "tests/test_task_queue.py",
    "tests/test_task_scheduler.py",
    "tests/test_task_state.py",
    "tests/test_context_components.py",
    "tests/test_context_manager.py",
    "tests/test_memory.py",
    "tests/test_memory_package.py",
    "tests/test_cort.py",
    "tests/test_metrics.py",
    "tests/test_message_model.py",
    "tests/test_agent_registry.py",
    "tests/test_async_loops.py",
    "tests/test_conftest.py",
    "tests/test_compile.py",
    "tests/test_benchmarks.py",
    "tests/test_system_integration.py",
]

# Pre-commit should avoid tests that require the rust_core extension (which is not
# built in a typical local pre-commit run) to keep commits fast and reliable.
PRECOMMIT_TEST_FILES = [
    "tests/test_core_agent_state_manager.py",
    "tests/test_core_agent_registry.py",
    "tests/test_core_helpers.py",
    "tests/test_core_observability.py",
    "tests/test_core_quality.py",
    "tests/test_core_runtime.py",
    "tests/test_core_task_queue.py",
    "tests/test_core_workflow_engine.py",
    "tests/test_workflow_engine.py",
    "tests/test_task.py",
    "tests/test_task_queue.py",
    "tests/test_task_scheduler.py",
    "tests/test_task_state.py",
    "tests/test_context_components.py",
    "tests/test_context_manager.py",
    "tests/test_cort.py",
    "tests/test_metrics.py",
    "tests/test_message_model.py",
    "tests/test_agent_registry.py",
    "tests/test_async_loops.py",
    "tests/test_conftest.py",
    "tests/test_compile.py",
    "tests/test_benchmarks.py",
]


def run_command(cmd: list[str], env: dict[str, str] | None = None) -> None:
    print(f"\n>>> Running: {' '.join(cmd)}\n")
    subprocess.run(cmd, check=True, env=env)


def run_ruff() -> None:
    run_command(["ruff", "check", "src", "tests"])
    run_command(["ruff", "format", "--check", "src", "tests"])


def run_mypy() -> None:
    run_command(["mypy", "--ignore-missing-imports", "src/core/base/"])


def run_pytest(files: list[str], extra_args: list[str] | None = None) -> None:
    cmd = ["python", "-m", "pytest", "-q", "--no-cov"] + files
    if extra_args:
        cmd += extra_args
    run_command(cmd)


def profile_precommit() -> None:
    """Quick checks suitable for pre-commit."""
    run_ruff()
    run_mypy()
    # Run a safe subset of core tests that do not depend on the rust extension.
    run_pytest(PRECOMMIT_TEST_FILES, extra_args=["-q"])


def profile_ci() -> None:
    """Full CI checks (equivalent to GitHub workflows).

    This is not intended to run on every local commit but provides a shared
    entrypoint for GitHub Actions to keep workflows consistent.
    """
    run_ruff()
    run_mypy()
    # Run the same core-suite as in ci-python-core.yml
    run_pytest(CORE_TEST_FILES, extra_args=["-q"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run shared sanity checks.")
    parser.add_argument(
        "--profile",
        choices=["precommit", "ci"],
        default="precommit",
        help="Which set of checks to run.",
    )
    args = parser.parse_args(argv)

    try:
        if args.profile == "precommit":
            profile_precommit()
        else:
            profile_ci()
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"\nERROR: command failed (exit {exc.returncode})\n")
        return exc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
