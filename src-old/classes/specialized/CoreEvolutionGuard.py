from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/CoreEvolutionGuard.description.md

# CoreEvolutionGuard

**File**: `src\classes\specialized\CoreEvolutionGuard.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 100  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for CoreEvolutionGuard.

## Classes (1)

### `CoreEvolutionGuard`

Monitors and validates changes to the agent's core source code.
Prevents unintended mutations or malicious injections into the agent logic.

**Methods** (5):
- `__init__(self, workspace_path)`
- `hash_file(self, file_path)`
- `snapshot_core_logic(self, core_paths)`
- `validate_code_integrity(self, file_path)`
- `generate_hardening_report(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `hashlib`
- `os`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/CoreEvolutionGuard.improvements.md

# Improvements for CoreEvolutionGuard

**File**: `src\classes\specialized\CoreEvolutionGuard.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 100 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CoreEvolutionGuard_test.py` with pytest tests

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


import hashlib
import os
import time
from typing import Any

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
from src.core.base.version import VERSION

__version__ = VERSION


class CoreEvolutionGuard:
    """Monitors and validates changes to the agent's core source code.
    Prevents unintended mutations or malicious injections into the agent logic.
    """

    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = workspace_path
        self.code_fingerprints: dict[str, str] = {}  # path -> hash
        self.security_threshold = 0.8

    def hash_file(self, file_path: str) -> str | None:
        """Calculates SHA256 hash of a file."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                buf = f.read()
                hasher.update(buf)
            return hasher.hexdigest()
        except FileNotFoundError:
            return None

    def snapshot_core_logic(self, core_paths: list[str]) -> dict[str, Any]:
        """Creates a baseline of hashes for critical agent files.
        """
        for path in core_paths:
            full_path = os.path.join(self.workspace_path, path)
            if os.path.exists(full_path):
                self.code_fingerprints[path] = self.hash_file(full_path)
            else:
                # Handle absolute paths if provided
                if os.path.isabs(path) and os.path.exists(path):
                    self.code_fingerprints[path] = self.hash_file(path)

        return {"monitored_files": len(self.code_fingerprints)}

    def validate_code_integrity(self, file_path: str) -> dict[str, Any]:
        """Validates if a change to a file is "safe" or needs human review.
        """
        # Determine relative path for lookup
        rel_path = file_path
        if os.path.isabs(file_path):
            try:
                rel_path = os.path.relpath(file_path, self.workspace_path)
            except ValueError:
                rel_path = file_path

        if rel_path not in self.code_fingerprints:
            return {"status": "untracked", "risk": "medium", "file": rel_path}

        full_path = (
            os.path.join(self.workspace_path, rel_path)
            if not os.path.isabs(rel_path)
            else rel_path
        )
        new_hash = self.hash_file(full_path)
        old_hash = self.code_fingerprints[rel_path]

        if new_hash == old_hash:
            return {"status": "unchanged", "risk": "none", "file": rel_path}

        # Simulated heuristic check
        # In a real scenario, this would analyze AST changes or use LLM classification
        risk = (
            "high"
            if "src/classes" in rel_path or "agent" in rel_path.lower()
            else "low"
        )

        return {
            "status": "modified",
            "risk": risk,
            "requires_review": True,
            "file": rel_path,
        }

    def generate_hardening_report(self) -> dict[str, Any]:
        """Returns a summary of the self-evolution guard status."""
        return {
            "uptime_integrity": 1.0,
            "failed_validations": 0,
            "last_scan": time.time(),
            "monitored_files_count": len(self.code_fingerprints),
        }
