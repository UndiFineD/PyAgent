# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/memory_mixins/MemoryStorageMixin.description.md

# MemoryStorageMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\memory_mixins\\MemoryStorageMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 50  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for MemoryStorageMixin.

## Classes (1)

### `MemoryStorageMixin`

Methods for storage and DB initialization.

**Methods** (4):
- `_init_db(self)`
- `save(self)`
- `load(self)`
- `clear(self)`

## Dependencies

**Imports** (4):
- `chromadb`
- `json`
- `logging`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/memory_mixins/MemoryStorageMixin.improvements.md

# Improvements for MemoryStorageMixin

**File**: `src\\logic\agents\\cognitive\\context\\engines\\memory_mixins\\MemoryStorageMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MemoryStorageMixin_test.py` with pytest tests

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

import json
import logging
from typing import Any

try:
    import chromadb

    HAS_CHROMA = True
except Exception:
    HAS_CHROMA = False


class MemoryStorageMixin:
    """Methods for storage and DB initialization."""

    def _init_db(self) -> Any:
        if not HAS_CHROMA:
            return None
        if self._collection:
            return self._collection
        try:
            client = chromadb.PersistentClient(path=str(self.db_path))
            self._collection = client.get_or_create_collection(name="agent_memory")
            return self._collection
        except Exception as e:
            logging.error(f"Memory DB init error: {e}")
            return None

    def save(self) -> None:
        """Persist memory to disk."""
        try:
            self.memory_file.write_text(json.dumps(self.episodes, indent=2))
        except Exception as e:
            logging.error(f"Failed to save memory: {e}")

    def load(self) -> None:
        """Load memory from disk."""
        if self.memory_file.exists():
            try:
                self.episodes = json.loads(self.memory_file.read_text())
            except Exception as e:
                logging.error(f"Failed to load memory: {e}")
                self.episodes = []

    def clear(self) -> None:
        """Wipe memory."""
        self.episodes = []
        if self.memory_file.exists():
            self.memory_file.unlink()
