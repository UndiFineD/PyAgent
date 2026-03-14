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

r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/security/external_recon_orchestrator.description.md

# external_recon_orchestrator

**File**: `src\\logic\agents\\security\\external_recon_orchestrator.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 6 imports  
**Lines**: 131  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for external_recon_orchestrator.

## Classes (2)

### `ReconConfig`

Class ReconConfig implementation.

### `ExternalReconOrchestrator`

Orchestrates external security tools similar to AutoRecon.

**Methods** (1):
- `__init__(self, config)`

## Dependencies

**Imports** (6):
- `asyncio`
- `dataclasses.dataclass`
- `os`
- `shutil`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/security/external_recon_orchestrator.improvements.md

# Improvements for external_recon_orchestrator

**File**: `src\\logic\agents\\security\\external_recon_orchestrator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 131 lines (medium)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Class Documentation
- [!] **1 undocumented classes**: ReconConfig

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `external_recon_orchestrator_test.py` with pytest tests

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
import asyncio
import os
import shutil
from dataclasses import dataclass
from typing import Optional

# Refactoring Note: Workflow ported from .external/0xSojalSec-AutoRecon/recon.sh
# This orchestration replaces the bash script with a Pythonic, async-capable flow.
# Actual binaries (nuclei, amass, etc.) must be installed in the system path.


@dataclass
class ReconConfig:
    domain: str
    results_path: str = "./results"
    use_amass: bool = True
    use_nuclei: bool = True
    threads: int = 5


class ExternalReconOrchestrator:
    """
    """
