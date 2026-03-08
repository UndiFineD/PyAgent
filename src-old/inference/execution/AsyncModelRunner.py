# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
LLM_CONTEXT_START

## Source: src-old/inference/execution/AsyncModelRunner.description.md

# AsyncModelRunner

**File**: `src\inference\execution\AsyncModelRunner.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 8 imports  
**Lines**: 25  
**Complexity**: 0 (simple)

## Overview

Facade for Async Model Runner modular implementation.

## Dependencies

**Imports** (8):
- `model_runner.AsyncGPUPoolingModelRunnerOutput`
- `model_runner.AsyncModelRunner`
- `model_runner.BatchedAsyncRunner`
- `model_runner.ExecutionPipeline`
- `model_runner.ModelInput`
- `model_runner.ModelOutput`
- `model_runner.RunnerState`
- `model_runner.SchedulerOutput`

---
*Auto-generated documentation*
## Source: src-old/inference/execution/AsyncModelRunner.improvements.md

# Improvements for AsyncModelRunner

**File**: `src\inference\execution\AsyncModelRunner.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 25 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AsyncModelRunner_test.py` with pytest tests

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

"""Facade for Async Model Runner modular implementation."""

from .model_runner import (
    RunnerState,
    ModelInput,
    ModelOutput,
    SchedulerOutput,
    AsyncGPUPoolingModelRunnerOutput,
    ExecutionPipeline,
    AsyncModelRunner,
    BatchedAsyncRunner,
)

__all__ = [
    "RunnerState",
    "ModelInput",
    "ModelOutput",
    "SchedulerOutput",
    "AsyncGPUPoolingModelRunnerOutput",
    "ExecutionPipeline",
    "AsyncModelRunner",
    "BatchedAsyncRunner",
]
