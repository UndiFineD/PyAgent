
"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/DependencyCore.description.md

# DependencyCore

**File**: `src\\logic\agents\\system\\core\\DependencyCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 81  
**Complexity**: 2 (simple)

## Overview

Core logic for Dependency Management (Phase 176).
Handles pip-audit execution and version pinning.

## Classes (1)

### `DependencyCore`

Class DependencyCore implementation.

**Methods** (2):
- `run_pip_audit(recorder)`
- `pin_requirements(file_path, recorder)`

## Dependencies

**Imports** (3):
- `os`
- `src.core.base.interfaces.ContextRecorderInterface`
- `subprocess`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/DependencyCore.improvements.md

# Improvements for DependencyCore

**File**: `src\\logic\agents\\system\\core\\DependencyCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 81 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: DependencyCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `DependencyCore_test.py` with pytest tests

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

"""
Core logic for Dependency Management (Phase 176).
Handles pip-audit execution and version pinning.
"""

import os
import subprocess

from src.core.base.interfaces import ContextRecorderInterface


class DependencyCore:
    @staticmethod
    def run_pip_audit(recorder: ContextRecorderInterface | None = None) -> str:
        """Runs pip-audit and returns the summary.
        """
        try:
            result = subprocess.run(["pip-audit", "--format", "plain"], capture_output=True, text=True)
            output = result.stdout or result.stderr
        except FileNotFoundError:
            output = "pip-audit not installed. Run 'pip install pip-audit' to enable."

        if recorder:
            recorder.record_interaction(
                provider="python",
                model="pip-audit",
                prompt="pip-audit --format plain",
                result=output[:2000]
            )

        return output

    @staticmethod
    def pin_requirements(file_path: str, recorder: ContextRecorderInterface | None = None) -> int:
        """Ensures all packages in a file are pinned with ==.
        Returns the number of lines modified.
        """
        if not os.path.exists(file_path):
            if recorder:
                recorder.record_interaction(
                    provider="python",
                    model="pip-freeze",
                    prompt=f"pin {file_path}",
                    result="file-not-found"
                )
            return 0

        with open(file_path) as f:
            lines = f.readlines()

        new_lines = []
        modified = 0
        for line in lines:
            stripped = line.strip()
            # If line is a package and not pinned
            if stripped and not stripped.startswith("#") and not stripped.startswith("-r"):
                if "==" not in stripped and ">=" not in stripped:
                    # In a real scenario, we'd fetch current version.
                    # For this phase, we'll mark it for review if not pinned.
                    new_lines.append(line.replace(stripped, stripped + "==LATEST-CHECK-REQUIRED"))
                    modified += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        with open(file_path, "w") as f:
            f.writelines(new_lines)

        if recorder:
            recorder.record_interaction(
                provider="python",
                model="pip-freeze",
                prompt=f"pin {file_path}",
                result=f"modified={modified}",
                meta={"changes": modified}
            )

        return modified
