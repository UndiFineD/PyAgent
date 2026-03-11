#!/usr/bin/env python3

"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/KnowledgeTransferEngine.description.md

# KnowledgeTransferEngine

**File**: `src\\classes\fleet\\KnowledgeTransferEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 50  
**Complexity**: 4 (simple)

## Overview

Engine for cross-fleet knowledge transfer.
Enables sharing lessons between decoupled fleet instances.

## Classes (1)

### `KnowledgeTransferEngine`

Manages export and import of knowledge/lessons between fleets.
Shell for KnowledgeTransferCore.

**Methods** (4):
- `__init__(self, workspace_root)`
- `export_knowledge(self, fleet_id, knowledge_data)`
- `import_knowledge(self, source_file)`
- `merge_lessons(self, current_lessons, imported_lessons)`

## Dependencies

**Imports** (7):
- `KnowledgeTransferCore.KnowledgeTransferCore`
- `json`
- `logging`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/KnowledgeTransferEngine.improvements.md

# Improvements for KnowledgeTransferEngine

**File**: `src\\classes\fleet\\KnowledgeTransferEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 50 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeTransferEngine_test.py` with pytest tests

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

"""Engine for cross-fleet knowledge transfer.
Enables sharing lessons between decoupled fleet instances.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from .KnowledgeTransferCore import KnowledgeTransferCore


class KnowledgeTransferEngine:
    """Manages export and import of knowledge/lessons between fleets.
    Shell for KnowledgeTransferCore.
    """

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.export_path = self.workspace_root / "knowledge_exports"
        self.export_path.mkdir(parents=True, exist_ok=True)
        self.core = KnowledgeTransferCore()

    def export_knowledge(self, fleet_id: str, knowledge_data: Dict[str, Any]) -> str:
        """Exports a fleet's knowledge (lessons, entities) to a shareable file."""
        export_file = self.export_path / f"knowledge_{fleet_id}.json"

        with open(export_file, "w") as f:
            json.dump(knowledge_data, f, indent=2)

        logging.info(f"KnowledgeTransfer: Exported knowledge for {fleet_id} to {export_file}")
        return str(export_file)

    def import_knowledge(self, source_file: str) -> Dict[str, Any]:
        """Imports knowledge from an external JSON file."""
        source_path = Path(source_file)
        if not source_path.exists():
            raise FileNotFoundError(f"Knowledge file not found: {source_file}")

        with open(source_path, "r") as f:
            data = json.load(f)

        logging.info(f"KnowledgeTransfer: Imported knowledge from {source_file}")
        return data

    def merge_lessons(self, current_lessons: List[Any], imported_lessons: List[Any]) -> List[Any]:
        """Merges imported lessons into the current set, avoiding duplicates."""
        return self.core.merge_lessons(current_lessons, imported_lessons)
