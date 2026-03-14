#!/usr/bin/env python3
r"""LLM_CONTEXT_START

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


r"""Auto-extracted class from agent.py"""
