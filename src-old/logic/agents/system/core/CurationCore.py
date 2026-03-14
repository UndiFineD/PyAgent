r"""LLM_CONTEXT_START

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
