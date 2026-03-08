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
LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/job_manager_core.description.md

# job_manager_core

**File**: `src\core\base\logic\core\job_manager_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 8 imports  
**Lines**: 62  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for job_manager_core.

## Classes (3)

### `JobStatus`

**Inherits from**: Enum

Class JobStatus implementation.

### `AgentJob`

Class AgentJob implementation.

### `JobManagerCore`

Manages the lifecycle of persistent agent jobs (sessions).
Harvested from LiveKit Agents patterns.

**Methods** (2):
- `__init__(self)`
- `get_job(self, job_id)`

## Dependencies

**Imports** (8):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/job_manager_core.improvements.md

# Improvements for job_manager_core

**File**: `src\core\base\logic\core\job_manager_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 62 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **2 undocumented classes**: JobStatus, AgentJob

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `job_manager_core_test.py` with pytest tests

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

import asyncio
import uuid
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentJob:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: JobStatus = JobStatus.PENDING
    payload: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None


class JobManagerCore:
    """
    Manages the lifecycle of persistent agent jobs (sessions).
    Harvested from LiveKit Agents patterns.
    """

    def __init__(self):
        self._jobs: Dict[str, AgentJob] = {}

    async def create_job(self, payload: Dict[str, Any]) -> str:
        job = AgentJob(payload=payload)
        self._jobs[job.id] = job
        return job.id

    async def update_job_status(
        self, job_id: str, status: JobStatus, result: Any = None, error: str = None
    ):
        if job_id in self._jobs:
            job = self._jobs[job_id]
            job.status = status
            if result is not None:
                job.result = result
            if error is not None:
                job.error = error

    def get_job(self, job_id: str) -> Optional[AgentJob]:
        return self._jobs.get(job_id)

    async def list_active_jobs(self) -> list[AgentJob]:
        return [
            j
            for j in self._jobs.values()
            if j.status in (JobStatus.PENDING, JobStatus.RUNNING)
        ]
