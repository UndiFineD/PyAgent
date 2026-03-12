#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/swarm/OrchestratorLifecycleMixin.description.md

# OrchestratorLifecycleMixin

**File**: `src\logic\agents\swarm\OrchestratorLifecycleMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 49  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for OrchestratorLifecycleMixin.

## Classes (1)

### `OrchestratorLifecycleMixin`

Health check and graceful shutdown methods for OrchestratorAgent.

**Methods** (5):
- `enable_graceful_shutdown(self)`
- `resume_from_shutdown(self)`
- `run_health_checks(self)`
- `is_healthy(self)`
- `print_health_report(self)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.GracefulShutdown.GracefulShutdown`
- `src.core.base.managers.SystemManagers.HealthChecker`
- `src.core.base.models.AgentHealthCheck`
- `src.core.base.models.HealthStatus`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/swarm/OrchestratorLifecycleMixin.improvements.md

# Improvements for OrchestratorLifecycleMixin

**File**: `src\logic\agents\swarm\OrchestratorLifecycleMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 49 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `OrchestratorLifecycleMixin_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import logging
from pathlib import Path
from src.core.base.models import AgentHealthCheck, HealthStatus
from src.core.base.GracefulShutdown import GracefulShutdown
from src.core.base.managers.SystemManagers import HealthChecker


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
