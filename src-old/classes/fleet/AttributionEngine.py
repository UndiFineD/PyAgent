#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/fleet/AttributionEngine.description.md

# AttributionEngine

**File**: `src\classes\fleet\AttributionEngine.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 95  
**Complexity**: 7 (moderate)

## Overview

Attribution Engine for PyAgent.
Tracks the lineage and provenance of every generated piece of content or code.

## Classes (1)

### `AttributionEngine`

Records the 'who, when, and how' for all system outputs (Phase 185).

**Methods** (7):
- `__init__(self, workspace_root)`
- `_load(self)`
- `apply_licensing(self, file_path)`
- `record_attribution(self, agent_id, content, task_context)`
- `_save(self)`
- `get_lineage(self, content_hash)`
- `get_summary(self)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `src.infrastructure.fleet.core.AttributionCore.AttributionCore`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/AttributionEngine.improvements.md

# Improvements for AttributionEngine

**File**: `src\classes\fleet\AttributionEngine.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 95 lines (small)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AttributionEngine_test.py` with pytest tests

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

from __future__ import annotations

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


"""Attribution Engine for PyAgent.
Tracks the lineage and provenance of every generated piece of content or code.
"""

from src.core.base.version import VERSION
import hashlib
import time
import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any
from src.infrastructure.fleet.core.AttributionCore import AttributionCore

__version__ = VERSION


class AttributionEngine:
    """Records the 'who, when, and how' for all system outputs (Phase 185)."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.log_file = self.workspace_root / "data/fleet/attribution_log.json"
        self.core = AttributionCore()
        os.makedirs(self.log_file.parent, exist_ok=True)
        self.records: list[dict[str, Any]] = self._load()

    def _load(self) -> list[dict[str, Any]]:
        if self.log_file.exists():
            with open(self.log_file) as f:
                return json.load(f)
        return []

    def apply_licensing(self, file_path: str) -> None:
        """Ensures the file has the correct license header (Phase 185)."""
        path = Path(file_path)
        if not path.exists():
            return

        with open(path, encoding="utf-8") as f:
            content = f.read()

        new_content = self.core.ensure_license_header(content)

        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            logging.info(f"AttributionEngine: Applied license header to {file_path}")

    def record_attribution(
        self, agent_id: str, content: str, task_context: str
    ) -> None:
        """Creates a record of content generation."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        record = {
            "timestamp": time.time(),
            "agent": agent_id,
            "hash": content_hash,
            "task": task_context,
            "metadata": {"chars": len(content), "words": len(content.split())},
        }
        self.records.append(record)
        self._save()

    def _save(self) -> None:
        with open(self.log_file, "w") as f:
            json.dump(self.records, f, indent=2)

    def get_lineage(self, content_hash: str) -> list[dict[str, Any]]:
        """Retrieves the history of a specific piece of content based on its hash."""
        return [r for r in self.records if r["hash"] == content_hash]

    def get_summary(self) -> dict[str, Any]:
        """Provides a summary of total attributions."""
        summary = {}
        for r in self.records:
            agent = r["agent"]
            summary[agent] = summary.get(agent, 0) + 1
        return summary
