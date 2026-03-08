#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/mixins/ContextShardMixin.description.md

# ContextShardMixin

**File**: `src\logic\agents\cognitive\context\engines\mixins\ContextShardMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 111  
**Complexity**: 4 (simple)

## Overview

Shard management logic for GlobalContextEngine.

## Classes (1)

### `ContextShardMixin`

Mixin for managing memory shards and persistence.

**Methods** (4):
- `_ensure_shard_loaded(self, category)`
- `load(self)`
- `save(self)`
- `trigger_rebalance(self)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `json`
- `logging`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/mixins/ContextShardMixin.improvements.md

# Improvements for ContextShardMixin

**File**: `src\logic\agents\cognitive\context\engines\mixins\ContextShardMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 111 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextShardMixin_test.py` with pytest tests

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

"""Shard management logic for GlobalContextEngine."""

import json
import logging


class ContextShardMixin:
    """Mixin for managing memory shards and persistence."""

    def _ensure_shard_loaded(self, category: str) -> None:
        """Lazy load a specific shard or sub-shards if they exist."""
        if not hasattr(self, "_loaded_shards") or category in self._loaded_shards:
            return None

        if not hasattr(self, "shard_dir") or not hasattr(self, "memory"):
            return None

        # Check for sub-shards (Phase 104)
        shard_files = list(self.shard_dir.glob(f"{category}_*.json"))
        if shard_files:
            if category not in self.memory:
                self.memory[category] = {}
            for s_file in shard_files:
                try:
                    shard_data = json.loads(s_file.read_text(encoding="utf-8"))
                    self.memory[category].update(shard_data)
                except Exception as e:
                    logging.warning(f"Failed to load sub-shard {s_file.name}: {e}")
            logging.info(
                f"Context: Loaded {len(shard_files)} sub-shards for '{category}'."
            )
        else:
            shard_file = self.shard_dir / f"{category}.json"
            if shard_file.exists():
                try:
                    shard_data = json.loads(shard_file.read_text(encoding="utf-8"))
                    self.memory[category] = shard_data
                    logging.info(f"Context: Lazy-loaded shard '{category}' from disk.")
                except Exception as e:
                    logging.warning(f"Failed to load shard {category}: {e}")

        self._loaded_shards.add(category)

    def load(self) -> None:
        """Loads default context state."""
        if (
            not hasattr(self, "context_file")
            or not hasattr(self, "memory")
            or not hasattr(self, "_loaded_shards")
        ):
            return

        if self.context_file.exists():
            try:
                data = json.loads(self.context_file.read_text(encoding="utf-8"))
                # Filter out what's in the default file
                self.memory.update(data)
                self._loaded_shards.add("default")
            except Exception as e:
                logging.error(f"Failed to load GlobalContext: {e}")

    def save(self) -> None:
        """Saves context to disk with optimization for large datasets."""
        if (
            not hasattr(self, "core")
            or not hasattr(self, "memory")
            or not hasattr(self, "context_file")
            or not hasattr(self, "shard_dir")
        ):
            return

        try:
            # Logic for sharding large datasets (Phase 101)
            # Phase 119: Adaptive rebalancing automatically scales shard count
            shards = self.core.partition_memory(self.memory, max_entries_per_shard=2000)

            # Phase 119: Check for shard bloat to notify system for potential migration
            bloated = self.core.detect_shard_bloat(shards)
            if bloated:
                logging.warning(
                    f"CONTEXT: Detected bloat in shards {bloated}. Adaptive rebalancing triggered."
                )

            # Save default state
            self.context_file.write_text(
                json.dumps(shards["default"], indent=2), encoding="utf-8"
            )

            # Save extra shards
            if len(shards) > 1:
                self.shard_dir.mkdir(exist_ok=True)
                for shard_name, shard_data in shards.items():
                    if shard_name == "default":
                        continue
                    shard_file = self.shard_dir / f"{shard_name}.json"
                    shard_file.write_text(
                        json.dumps(shard_data, indent=2), encoding="utf-8"
                    )

        except Exception as e:
            logging.error(f"Failed to save GlobalContext: {e}")

    def trigger_rebalance(self) -> None:
        """Manually force a rebalancing of the context shards."""
        logging.info("CONTEXT: Triggering manual shard rebalancing...")
        self.save()
