#!/usr/bin/env python3

"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/SchemaManager.description.md

# SchemaManager

**File**: `src\\classes\fleet\\SchemaManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 31  
**Complexity**: 4 (simple)

## Overview

Fleet-wide manager for database schema discovery and metadata storage.

## Classes (1)

### `SchemaManager`

Discovers and caches database schemas across the fleet.

**Methods** (4):
- `__init__(self)`
- `register_schema(self, db_id, tables)`
- `get_context_for_agent(self, db_id)`
- `list_known_databases(self)`

## Dependencies

**Imports** (4):
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/SchemaManager.improvements.md

# Improvements for SchemaManager

**File**: `src\\classes\fleet\\SchemaManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 31 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SchemaManager_test.py` with pytest tests

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

"""Fleet-wide manager for database schema discovery and metadata storage."""

import logging
from typing import Any, Dict, List


class SchemaManager:
    """Discovers and caches database schemas across the fleet."""

    def __init__(self) -> None:
        self.schemas: Dict[str, Dict[str, Any]] = {}  # db_path -> schema_map

    def register_schema(self, db_id: str, tables: Dict[str, List[str]]) -> str:
        """Registers a database schema (tables and columns)."""
        self.schemas[db_id] = tables
        logging.info(
            f"SchemaManager: Registered schema for {db_id} with {len(tables)} tables."
        )

    def get_context_for_agent(self, db_id: str) -> str:
        """Generates a schema summary for an agent's system prompt."""
        if db_id not in self.schemas:
            return "No schema information available."

        summary = [f"Database: {db_id}"]
        for table, cols in self.schemas[db_id].items():
            summary.append(f"- Table: {table} (Columns: {', '.join(cols)})")
        return "\n".join(summary)

    def list_known_databases(self) -> List[str]:
        """Returns IDs of all registered databases."""
        return list(self.schemas.keys())
