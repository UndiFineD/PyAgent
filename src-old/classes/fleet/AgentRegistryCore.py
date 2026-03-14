#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/AgentRegistryCore.description.md

# AgentRegistryCore

**File**: `src\\classes\fleet\\AgentRegistryCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 79  
**Complexity**: 5 (moderate)

## Overview

AgentRegistryCore logic for version compatibility and manifest validation.
Pure logic component to be potentially rustified.

## Classes (1)

### `AgentRegistryCore`

Pure logic core for Agent Registry.

**Methods** (5):
- `__init__(self, current_sdk_version)`
- `process_discovered_files(self, file_paths)`
- `parse_manifest(self, raw_manifest)`
- `is_compatible(self, required_version)`
- `validate_agent_structure(self, agent_instance, required_methods)`

## Dependencies

**Imports** (7):
- `VersionGate.VersionGate`
- `os`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/AgentRegistryCore.improvements.md

# Improvements for AgentRegistryCore

**File**: `src\\classes\fleet\\AgentRegistryCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 79 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentRegistryCore_test.py` with pytest tests

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

"""
AgentRegistryCore logic for version compatibility and manifest validation.
Pure logic component to be potentially rustified.
"""
import os
from typing import Any, Dict, List, Optional, Tuple

from .VersionGate import VersionGate


class AgentRegistryCore:
    """
    """
