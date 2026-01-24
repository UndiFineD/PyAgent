#!/usr/bin/env python3

"""
Orchestrator lifecycle mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

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
