#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .AgentHealthCheck import AgentHealthCheck
from .HealthStatus import HealthStatus

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

class HealthChecker:
    """Performs health checks on agent components.

    Verifies that all required components are available and functional
    before starting agent execution.

    Attributes:
        repo_root: Repository root directory.
        results: Dict of health check results.
    """

    def __init__(self, repo_root: Path) -> None:
        """Initialize the health checker.

        Args:
            repo_root: Repository root directory.
        """
        self.repo_root = repo_root
        self.results: Dict[str, AgentHealthCheck] = {}

    def check_agent_script(self, agent_name: str) -> AgentHealthCheck:
        """Check if an agent script exists and is valid.

        Args:
            agent_name: Name of the agent (e.g., 'coder', 'tests').

        Returns:
            AgentHealthCheck result.
        """
        start_time = time.time()
        # Look for script in src/ directory (scripts are stored there)
        script_path = Path(__file__).parent.parent.parent / f'agent_{agent_name}.py'

        if not script_path.exists():
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Script not found: {script_path}"
            )

        # Check if script is valid Python
        try:
            import ast
            content = script_path.read_text(encoding='utf-8', errors='ignore')
            ast.parse(content)
            response_time = (time.time() - start_time) * 1000
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.HEALTHY,
                response_time_ms=response_time,
                details={'script_path': str(script_path)}
            )
        except SyntaxError as e:
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Syntax error: {e}"
            )

    def check_git(self) -> AgentHealthCheck:
        """Check if git is available.

        Returns:
            AgentHealthCheck result.
        """
        start_time = time.time()

        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            response_time = (time.time() - start_time) * 1000

            if result.returncode == 0:
                return AgentHealthCheck(
                    agent_name='git',
                    status=HealthStatus.HEALTHY,
                    response_time_ms=response_time,
                    details={'version': result.stdout.strip()}
                )
            else:
                return AgentHealthCheck(
                    agent_name='git',
                    status=HealthStatus.UNHEALTHY,
                    error_message=result.stderr
                )
        except Exception as e:
            return AgentHealthCheck(
                agent_name='git',
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )

    def check_python(self) -> AgentHealthCheck:
        """Check Python environment.

        Returns:
            AgentHealthCheck result.
        """
        start_time = time.time()
        response_time = (time.time() - start_time) * 1000

        return AgentHealthCheck(
            agent_name='python',
            status=HealthStatus.HEALTHY,
            response_time_ms=response_time,
            details={
                'version': sys.version,
                'executable': sys.executable
            }
        )

    def run_all_checks(self) -> Dict[str, AgentHealthCheck]:
        """Run all health checks.

        Returns:
            Dict of check name to AgentHealthCheck result.
        """
        agent_names = ['coder', 'tests', 'changes', 'context', 'errors',
                       'improvements', 'stats']

        # Check core components
        self.results['python'] = self.check_python()
        self.results['git'] = self.check_git()

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

        return all(
            r.status == HealthStatus.HEALTHY
            for r in self.results.values()
        )

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
                HealthStatus.UNKNOWN: "?"
            }.get(result.status, "?")

            print(f"  [{status_symbol}] {name}: {result.status.name}")
            if result.error_message:
                print(f"      Error: {result.error_message}")
            if result.response_time_ms > 0:
                print(f"      Response: {result.response_time_ms:.1f}ms")

        print()
