#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/agent/HealthChecker.description.md

# HealthChecker

**File**: `src\\classes\agent\\HealthChecker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 40 imports  
**Lines**: 210  
**Complexity**: 8 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `HealthChecker`

Performs health checks on agent components.

Verifies that all required components are available and functional
before starting agent execution.

Attributes:
    repo_root: Repository root directory.
    results: Dict of health check results.

**Methods** (8):
- `__init__(self, repo_root, recorder)`
- `_record(self, action, result)`
- `check_agent_script(self, agent_name)`
- `check_git(self)`
- `check_python(self)`
- `run_all_checks(self)`
- `is_healthy(self)`
- `print_report(self)`

## Dependencies

**Imports** (40):
- `AgentHealthCheck.AgentHealthCheck`
- `HealthStatus.HealthStatus`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `argparse`
- `ast`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `difflib`
- `enum.Enum`
- `enum.auto`
- ... and 25 more

---
*Auto-generated documentation*
## Source: src-old/classes/agent/HealthChecker.improvements.md

# Improvements for HealthChecker

**File**: `src\\classes\agent\\HealthChecker.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 210 lines (medium)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `HealthChecker_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END

"""

from __future__ import annotations

"""Auto-extracted class from agent.py"""


import subprocess
import sys
import time
from pathlib import Path
from typing import (
    Any,
    Dict,
)

from .AgentHealthCheck import AgentHealthCheck
from .HealthStatus import HealthStatus


class HealthChecker:
    """Performs health checks on agent components.

    Verifies that all required components are available and functional
    before starting agent execution.

    Attributes:
        repo_root: Repository root directory.
        results: Dict of health check results.

    """

    def __init__(self, repo_root: Path, recorder: Any = None) -> None:
        """Initialize the health checker.

        Args:
            repo_root: Repository root directory.
            recorder: Optional LocalContextRecorder.

        """
        self.repo_root = repo_root
        self.recorder = recorder
        self.results: Dict[str, AgentHealthCheck] = {}

    def _record(self, action: str, result: str) -> None:
        """Record health check activities."""
        if self.recorder:
            self.recorder.record_interaction("HealthCheck", "CLI", action, result)

    def check_agent_script(self, agent_name: str) -> AgentHealthCheck:
        """Check if an agent script exists and is valid.

        Args:
            agent_name: Name of the agent (e.g., 'coder', 'tests').

        Returns:
            AgentHealthCheck result.

        """
        start_time = time.time()
        # Look for script in src/ directory (scripts are stored there)
        script_path = Path(__file__).parent.parent.parent / f"agent_{agent_name}.py"

        if not script_path.exists():
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Script not found: {script_path}",
            )

        # Check if script is valid Python
        try:
            import ast

            content = script_path.read_text(encoding="utf-8", errors="ignore")
            ast.parse(content)
            response_time = (time.time() - start_time) * 1000
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.HEALTHY,
                response_time_ms=response_time,
                details={"script_path": str(script_path)},
            )
        except SyntaxError as e:
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Syntax error: {e}",
            )

    def check_git(self) -> AgentHealthCheck:
        """Check if git is available.

        Returns:
            AgentHealthCheck result.

        """
        start_time = time.time()

        try:
            result = subprocess.run(
                ["git", "--version"], capture_output=True, text=True, timeout=5
            )
            response_time = (time.time() - start_time) * 1000

            if result.returncode == 0:
                return AgentHealthCheck(
                    agent_name="git",
                    status=HealthStatus.HEALTHY,
                    response_time_ms=response_time,
                    details={"version": result.stdout.strip()},
                )
            else:
                return AgentHealthCheck(
                    agent_name="git",
                    status=HealthStatus.UNHEALTHY,
                    error_message=result.stderr,
                )
        except Exception as e:
            return AgentHealthCheck(
                agent_name="git", status=HealthStatus.UNHEALTHY, error_message=str(e)
            )

    def check_python(self) -> AgentHealthCheck:
        """Check Python environment.

        Returns:
            AgentHealthCheck result.

        """
        start_time = time.time()
        response_time = (time.time() - start_time) * 1000

        return AgentHealthCheck(
            agent_name="python",
            status=HealthStatus.HEALTHY,
            response_time_ms=response_time,
            details={"version": sys.version, "executable": sys.executable},
        )

    def run_all_checks(self) -> Dict[str, AgentHealthCheck]:
        """Run all health checks.

        Returns:
            Dict of check name to AgentHealthCheck result.

        """
        agent_names = [
            "coder",
            "tests",
            "changes",
            "context",
            "errors",
            "improvements",
            "stats",
        ]

        # Check core components
        self.results["python"] = self.check_python()
        self.results["git"] = self.check_git()

        # Check agent scripts
        for name in agent_names:
            self.results[name] = self.check_agent_script(name)

        return self.results

    def is_healthy(self) -> bool:
        """Check if all components are healthy.

        Returns:
            bool: True if all healthy, False otherwise.

        """
        if not self.results:
            self.run_all_checks()

        return all(r.status == HealthStatus.HEALTHY for r in self.results.values())

    def print_report(self) -> None:
        """Print health check report."""
        if not self.results:
            self.run_all_checks()

        print("\n=== Agent Health Check Report ===\n")
        for name, result in sorted(self.results.items()):
            status_symbol = {
                HealthStatus.HEALTHY: "✓",
                HealthStatus.DEGRADED: "!",
                HealthStatus.UNHEALTHY: "✗",
                HealthStatus.UNKNOWN: "?",
            }.get(result.status, "?")

            print(f"  [{status_symbol}] {name}: {result.status.name}")
            if result.error_message:
                print(f"      Error: {result.error_message}")
            if result.response_time_ms > 0:
                print(f"      Response: {result.response_time_ms:.1f}ms")

        print()
