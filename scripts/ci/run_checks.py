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
import os
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
    # Quality/metadata tests (previously run in ci-python-quality.yml).
    "tests/test_quality_yaml.py",
    # no need to duplicate these test
    # "tests/test_precommit.py"
    # "tests/test_coverage_meta.py"
    # no need to duplicate these test
    # "tests/zzz/test_zza_lint_config.py",
    # "tests/zzz/test_zzb_mypy_config.py",
    # "tests/zzz/ztest_zzz_tests_quality.py",
    # CodeQL SARIF gate (also in CODEQL_TEST_FILES, included here for full CI)
    "tests/zzz/test_zze_codeql_javascript.py",
    "tests/zzz/test_zzf_codeql_rust.py",
    "tests/zzz/test_zzg_codeql_sarif_gate.py",
    "tests/zzz/test_zzd_codeql_python.py",
]

# CodeQL SARIF gate tests — fast (read-only JSON checks, no rebuild).
# The per-language rebuild tests (zzd/e/f) are listed here but skip automatically
# when SARIF is fresh; they only rebuild when SARIF is missing or >24h old.
CODEQL_TEST_FILES = [
    "tests/zzz/test_zzd_codeql_python.py",
    "tests/zzz/test_zze_codeql_javascript.py",
    "tests/zzz/test_zzf_codeql_rust.py",
    "tests/zzz/test_zzg_codeql_sarif_gate.py",
]


def run_command(cmd: list[str], env: dict[str, str] | None = None) -> None:
    """Run a command with optional environment variables, printing it first."""
    print(f"\n>>> Running: {' '.join(cmd)}\n")
    merged_env = os.environ.copy()
    merged_env.setdefault("PYTHONNOUSERSITE", "1")
    if env:
        merged_env.update(env)
    subprocess.run(cmd, check=True, env=merged_env)  # noqa: S603


def _repo_venv_python() -> Path:
    """Return repository venv Python path for current platform."""
    if os.name == "nt":
        return Path(".venv") / "Scripts" / "python.exe"
    return Path(".venv") / "bin" / "python"


def _ensure_repo_venv_interpreter(argv: list[str]) -> int | None:
    """Re-run under repository .venv Python when available.

    This avoids interpreter/package drift when pre-commit resolves to a different
    Python than the repository runtime environment.
    """
    if os.environ.get("PYAGENT_RUN_CHECKS_BOOTSTRAPPED") == "1":
        return None

    target = _repo_venv_python().resolve()
    if not target.exists():
        return None

    current = Path(sys.executable).resolve()
    if current == target:
        return None

    env = os.environ.copy()
    env["PYAGENT_RUN_CHECKS_BOOTSTRAPPED"] = "1"
    env.setdefault("PYTHONNOUSERSITE", "1")
    script_path = str(Path(__file__).resolve())
    result = subprocess.run([str(target), script_path, *argv], env=env, check=False)  # noqa: S603
    return int(result.returncode)


def _filter_python_targets(paths: list[str]) -> list[str]:
    """Filter incoming paths to Python files under supported source roots."""
    allowed_roots = ("src/", "tests/", "scripts/", "docs/")
    filtered: list[str] = []
    for raw in paths:
        normalized = raw.replace("\\", "/")
        if normalized.endswith(".py") and normalized.startswith(allowed_roots):
            filtered.append(normalized)
    return filtered


def run_ruff(paths: list[str] | None = None) -> None:
    """Run ruff checks and formatting checks.

    When explicit paths are provided (as in pre-commit), lint only those files to
    avoid unrelated repository lint debt blocking scoped project commits.
    """
    targets = _filter_python_targets(paths or [])
    if targets:
        run_command(["ruff", "check", *targets])
        run_command(["ruff", "format", "--check", *targets])
        return

    run_command(["ruff", "check", "src", "tests"])
    run_command(["ruff", "format", "--check", "src", "tests"])


def run_mypy() -> None:
    """Run mypy type checks."""
    run_command([sys.executable, "-m", "mypy", "--ignore-missing-imports", "src/core/base/"])


def run_dependency_sync_gate() -> None:
    """Run dependency parity/policy gate for pyproject/requirements sync."""
    run_command([sys.executable, "-m", "src.tools.dependency_audit", "--root", ".", "--check"])


def run_pytest(files: list[str], extra_args: list[str] | None = None) -> None:
    """Run pytest on the given list of test files with optional extra arguments."""
    cmd = [sys.executable, "-m", "pytest", "-q", "--no-cov"] + files
    if extra_args:
        cmd += extra_args
    run_command(cmd)


def profile_precommit(paths: list[str] | None = None) -> None:
    """Quick checks suitable for pre-commit."""
    run_dependency_sync_gate()
    run_ruff(paths)
    run_mypy()
    # Run a safe subset of core tests that do not depend on the rust extension.
    run_pytest(PRECOMMIT_TEST_FILES, extra_args=["-q"])
    # CodeQL security gate: SARIF must be fresh and contain no hard-fail findings.
    # Individual DB rebuilds are skipped automatically when SARIF is < 24h old.
    run_pytest(CODEQL_TEST_FILES, extra_args=["-q"])


def profile_ci() -> None:
    """Full CI checks (equivalent to GitHub workflows).

    This is not intended to run on every local commit but provides a shared
    entrypoint for GitHub Actions to keep workflows consistent.
    """
    run_dependency_sync_gate()
    run_ruff()
    run_mypy()
    # Run the same core-suite as in ci-python-core.yml
    run_pytest(CORE_TEST_FILES, extra_args=["-q"])


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the checks script."""
    forwarded_argv = list(argv) if argv is not None else sys.argv[1:]
    bootstrap_rc = _ensure_repo_venv_interpreter(forwarded_argv)
    if bootstrap_rc is not None:
        return bootstrap_rc

    parser = argparse.ArgumentParser(description="Run shared sanity checks.")
    parser.add_argument(
        "--profile",
        choices=["precommit", "ci"],
        default="precommit",
        help="Which set of checks to run.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional file paths to scope pre-commit checks.",
    )
    args = parser.parse_args(argv)

    try:
        if args.profile == "precommit":
            profile_precommit(args.paths)
        else:
            profile_ci()
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"\nERROR: command failed (exit {exc.returncode})\n")
        return exc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
