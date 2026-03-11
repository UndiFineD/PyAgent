# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""LLM_CONTEXT_START

## Source: src-old/core/base/verification/ConfigValidator.description.md

# ConfigValidator

**File**: `src\\core\base\verification\\ConfigValidator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 38  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for ConfigValidator.

## Classes (1)

### `ConfigValidator`

Phase 278: Validates configuration files and detects orphaned references.

**Methods** (1):
- `validate_shard_mapping(mapping_path)`

## Dependencies

**Imports** (3):
- `json`
- `logging`
- `pathlib.Path`

---
*Auto-generated documentation*
## Source: src-old/core/base/verification/ConfigValidator.improvements.md

# Improvements for ConfigValidator

**File**: `src\\core\base\verification\\ConfigValidator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 38 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConfigValidator_test.py` with pytest tests

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

import json
import logging
from pathlib import Path


class ConfigValidator:
    """Phase 278: Validates configuration files and detects orphaned references."""

    @staticmethod
    def validate_shard_mapping(
        mapping_path: Path = Path("data/config/shard_mapping.json"),
    ) -> list[str]:
        """Checks shard_mapping.json for orphaned AgentIDs."""
        if not mapping_path.exists():
            logging.warning(
                f"ConfigValidator: {mapping_path} not found. Skipping validation."
            )
            return []

        orphans = []
        try:
            mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
            # Heuristic: Check if the agent folder exists in src/ (just a demo check)

            for agent_id in mapping.get("agents", {}).keys():
                agent_dir = Path("src/logic/agents") / agent_id
                if not agent_dir.exists():
                    orphans.append(agent_id)
                    logging.error(
                        f"ConfigValidator: Orphaned agent reference detected: {agent_id}"
                    )

        except Exception as e:
            logging.error(f"ConfigValidator: Failed to validate shard mapping: {e}")

        return orphans
