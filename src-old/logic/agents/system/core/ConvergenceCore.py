"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/ConvergenceCore.description.md

# ConvergenceCore

**File**: `src\\logic\agents\\system\\core\\ConvergenceCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 51  
**Complexity**: 2 (simple)

## Overview

Core logic for Swarm Convergence (Phase 170).
Handles file system cleanup and version management.

## Classes (1)

### `ConvergenceCore`

Class ConvergenceCore implementation.

**Methods** (2):
- `clean_sweep(root_dir)`
- `update_version_file(file_path, new_version)`

## Dependencies

**Imports** (3):
- `os`
- `re`
- `shutil`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/ConvergenceCore.improvements.md

# Improvements for ConvergenceCore

**File**: `src\\logic\agents\\system\\core\\ConvergenceCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 51 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: ConvergenceCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConvergenceCore_test.py` with pytest tests

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
Core logic for Swarm Convergence (Phase 170).
Handles file system cleanup and version management.
"""

import os
import re
import shutil


class ConvergenceCore:
    @staticmethod
    def clean_sweep(root_dir: str) -> dict:
        """Removes __pycache__ and temporary files.
        """
        stats = {"pycache_removed": 0, "tmp_removed": 0}

        for root, dirs, files in os.walk(root_dir):
            # Remove __pycache__
            if "__pycache__" in dirs:
                shutil.rmtree(os.path.join(root, "__pycache__"))
                stats["pycache_removed"] += 1
                dirs.remove("__pycache__")

            # Remove .tmp files
            for file in files:
                if file.endswith(".tmp") or file.endswith(".temp"):
                    os.remove(os.path.join(root, file))
                    stats["tmp_removed"] += 1

        return stats

    @staticmethod
    def update_version_file(file_path: str, new_version: str) -> bool:
        """Updates the version string in version.py.
        """
        if not os.path.exists(file_path):
            return False

        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Regex to find VERSION = "..."
        new_content = re.sub(
            r'VERSION\s*=\s*["\'].*?["\']', f'VERSION = "{new_version}"', content
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return True
