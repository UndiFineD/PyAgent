"""LLM_CONTEXT_START

## Source: src-old/logic/agents/system/core/CurationCore.description.md

# CurationCore

**File**: `src\\logic\agents\\system\\core\\CurationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 48  
**Complexity**: 2 (simple)

## Overview

Core logic for Resource Curation (Phase 173).
Handles pruning of temporary directories and old files.

## Classes (1)

### `CurationCore`

Class CurationCore implementation.

**Methods** (2):
- `prune_directory(directory, max_age_days)`
- `deep_clean_pycache(root_dir)`

## Dependencies

**Imports** (3):
- `os`
- `shutil`
- `time`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/system/core/CurationCore.improvements.md

# Improvements for CurationCore

**File**: `src\\logic\agents\\system\\core\\CurationCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 48 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Class Documentation
- [!] **1 undocumented classes**: CurationCore

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CurationCore_test.py` with pytest tests

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
Core logic for Resource Curation (Phase 173).
Handles pruning of temporary directories and old files.
"""

import os
import shutil
import time


class CurationCore:
    @staticmethod
    def prune_directory(directory: str, max_age_days: int = 7) -> int:
        """Removes files in a directory that are older than max_age_days.
        Returns the number of files removed.
        """
        if not os.path.exists(directory):
            return 0

        count = 0
        now = time.time()
        max_age_seconds = max_age_days * 86400

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if now - os.path.getmtime(file_path) > max_age_seconds:
                        os.remove(file_path)
                        count += 1
                except OSError:
                    continue

        return count

    @staticmethod
    def deep_clean_pycache(root_dir: str) -> int:
        """Forcefully removes all __pycache__ folders.
        """
        count = 0
        for root, dirs, files in os.walk(root_dir):
            if "__pycache__" in dirs:
                shutil.rmtree(os.path.join(root, "__pycache__"))
                count += 1
                dirs.remove("__pycache__")
        return count
