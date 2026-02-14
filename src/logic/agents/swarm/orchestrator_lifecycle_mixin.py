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
OrchestratorLifecycleMixin - Health checking and graceful shutdown for OrchestratorAgent

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Mix into an OrchestratorAgent class to add lifecycle utilities
- Call enable_graceful_shutdown to install OS signal handlers and persist resume state
- Use resume_from_shutdown to recover pending work, run_health_checks or print_health_report for diagnostics, and is_healthy to gate operations

WHAT IT DOES:
- Provides enable_graceful_shutdown to register GracefulShutdown tied to repo_root
- Provides resume_from_shutdown to load persisted resume state and return pending file paths
- Provides run_health_checks to execute HealthChecker run_all_checks and return AgentHealthCheck results
- Provides is_healthy to evaluate overall health by comparing check results to HealthStatus.HEALTHY
- Provides print_health_report to execute checks and emit a human-readable report via HealthChecker

WHAT IT SHOULD DO BETTER:
- Accept dependency injection for GracefulShutdown and HealthChecker to improve testability and avoid repeated instantiation
- Surface exceptions and add richer logging and metrics for failure modes rather than silent returns
- Add async variants and cancellation support to integrate with asyncio-based OrchestratorAgents
- Improve type consistency by annotating return types uniformly and returning empty lists instead of None where appropriate
- Add unit tests and clearer docstrings per-method and integrate CascadeContext and StateTransaction where lifecycle persistence is used

FILE CONTENT SUMMARY:
Orchestrator lifecycle mixin.py module.
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.core.base.common.models import AgentHealthCheck, HealthStatus
from src.core.base.lifecycle.graceful_shutdown import GracefulShutdown
from src.core.base.logic.managers.system_managers import HealthChecker


class OrchestratorLifecycleMixin:
    """Health check and graceful shutdown methods for OrchestratorAgent."""

    def enable_graceful_shutdown(self) -> None:
        """Enable graceful shutdown."""
        repo_root = getattr(self, "repo_root", Path("."))
        self.shutdown_handler = GracefulShutdown(repo_root)
        self.shutdown_handler.install_handlers()
        logging.info("Graceful shutdown enabled")

    def resume_from_shutdown(self) -> list[Path] | None:
        """Resume from interrupted state."""
        repo_root = getattr(self, "repo_root", Path("."))
        if not hasattr(self, "shutdown_handler"):
            self.shutdown_handler = GracefulShutdown(repo_root)
        state = self.shutdown_handler.load_resume_state()
        if state and state.pending_files:
            return [Path(f) for f in state.pending_files]
        return None

    def run_health_checks(self) -> dict[str, AgentHealthCheck]:
        """Run health checks."""
        repo_root = getattr(self, "repo_root", Path("."))
        checker = HealthChecker(repo_root)
        return checker.run_all_checks()

    def is_healthy(self) -> bool:
        """Check if all components are healthy."""
        results = self.run_health_checks()
        return all(r.status == HealthStatus.HEALTHY for r in results.values())

    def print_health_report(self) -> None:
        """Print a health report."""
        repo_root = getattr(self, "repo_root", Path("."))
        checker = HealthChecker(repo_root)
        checker.run_all_checks()
        checker.print_report()
