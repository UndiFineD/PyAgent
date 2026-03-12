"""
LLM_CONTEXT_START

## Source: src-old/classes/backend/LocalContextRecorder.description.md

# LocalContextRecorder

**File**: `src\classes\backend\LocalContextRecorder.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 137  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for LocalContextRecorder.

## Classes (1)

### `LocalContextRecorder`

**Inherits from**: ContextRecorderInterface

Records LLM prompts and results for future training/fine-tuning.
Stores data in JSONL format with monthly and hash-based sharding.
Optimized for trillion-parameter data harvesting (Phase 105).

**Methods** (4):
- `__init__(self, workspace_root, user_context, fleet)`
- `record_interaction(self, provider, model, prompt, result, meta)`
- `record_lesson(self, tag, data)`
- `_update_index(self, prompt_hash, filename)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `datetime.datetime`
- `gzip`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.BaseInterfaces.ContextRecorderInterface`
- `src.core.base.Version.VERSION`
- `src.core.rust_bridge.RustBridge`
- `typing.Any`
- `zlib`

---
*Auto-generated documentation*
## Source: src-old/classes/backend/LocalContextRecorder.improvements.md

# Improvements for LocalContextRecorder

**File**: `src\classes\backend\LocalContextRecorder.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 137 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `LocalContextRecorder_test.py` with pytest tests

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


from src.core.base.Version import VERSION
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from src.core.base.BaseInterfaces import ContextRecorderInterface

__version__ = VERSION


class LocalContextRecorder(ContextRecorderInterface):
    """
    Records LLM prompts and results for future training/fine-tuning.
    Stores data in JSONL format with monthly and hash-based sharding.
    Optimized for trillion-parameter data harvesting (Phase 105).
    """

    def __init__(
        self,
        workspace_root: Path | None = None,
        user_context: str = "System",
        fleet: Any = None,
    ) -> None:
        if fleet and hasattr(fleet, "workspace_root"):
            self.workspace_root = Path(fleet.workspace_root)
        elif workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path(".")

        self.user_context = user_context
        self.log_dir = self.workspace_root / "data/logs" / "external_ai_learning"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        # Phase 319: Global sharding scale (1,024 shards)
        self.shard_count = 1024
        self.current_month = datetime.now().strftime("%Y%m")
        self.use_compression = True  # Save 70-80% space for massive datasets

    def record_interaction(
        self,
        provider: str,
        model: str,
        prompt: str,
        result: str,
        meta: dict[str, Any] | None = None,
    ) -> None:
        """
        Appends a new interaction record.
        Includes unique context hashing for future deduplication and sharded storage.
        Optimized for high-throughput and low-latency disk writes.
        """
        import hashlib
        import zlib
        import gzip

        # Stability: generate a stable hash for the prompt to allow O(1) deduplication
        prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

        # Phase 318: Audited Rust MD5 Sharding
        from src.core.rust_bridge import RustBridge

        shard_id = RustBridge.calculate_shard_id(prompt_hash, self.shard_count)

        # Use .jsonl.gz if compression is enabled
        ext = ".jsonl.gz" if self.use_compression else ".jsonl"
        log_file = self.log_dir / f"shard_{self.current_month}_{shard_id:03d}{ext}"

        record = {
            "timestamp": datetime.now().isoformat(),
            "user_context": self.user_context,
            "provider": provider,
            "model": model,
            "prompt_hash": prompt_hash,
            "prompt": prompt,
            "result": result,
            "meta": meta or {},
        }

        # Handle non-serializable objects (like MagicMocks in tests)
        def _safe_serialize(obj: Any) -> Any:
            try:
                if isinstance(obj, (int, float, str, bool, type(None))):
                    return obj
                return str(obj)
            except Exception:
                return f"<unserializable {type(obj).__name__}>"

        try:
            if self.use_compression:
                line = (json.dumps(record, default=_safe_serialize) + "\n").encode(
                    "utf-8"
                )
                with gzip.open(log_file, "ab") as f:
                    f.write(line)
            else:
                line_str = json.dumps(record, default=_safe_serialize) + "\n"
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(line_str)

            # Update a centralized index for fast semantic lookup in the future (Phase 106)
            self._update_index(prompt_hash, str(log_file.name))

        except Exception as e:
            logging.error(f"Failed to record interaction to shard {shard_id}: {e}")

    def record_lesson(self, tag: str, data: dict[str, Any]) -> None:
        """Alias for general logic harvesting to satisfy intelligence scanners."""
        self.record_interaction(
            provider="Internal",
            model=tag,
            prompt=json.dumps(data),
            result="Harvested",
            meta={"tag": tag},
        )

    def _update_index(self, prompt_hash: str, filename: str) -> None:
        """Simple index updates to avoid scanning all shards for a specific query."""
        index_file = self.log_dir / "shards_lookup.index"
        try:
            # Atomic append for the index
            with open(index_file, "a", encoding="utf-8") as f:
                f.write(f"{prompt_hash}:{filename}\n")
        except Exception as e:
            logging.error(f"Failed to update shard index: {e}")
