"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/utils/GlobalContextCore.description.md

# GlobalContextCore

**File**: `src\logic\agents\cognitive\context\utils\GlobalContextCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 85  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for GlobalContextCore.

## Classes (1)

### `GlobalContextCore`

Pure logic for GlobalContext.
Handles data merging, pruning, and summary formatting.
No I/O or direct disk access.

**Methods** (6):
- `partition_memory(self, memory, max_entries_per_shard)`
- `prepare_fact(self, key, value)`
- `prepare_insight(self, insight, source_agent)`
- `merge_entity_info(self, existing, new_attributes)`
- `prune_lessons(self, lessons, max_lessons)`
- `generate_markdown_summary(self, memory)`

## Dependencies

**Imports** (6):
- `datetime.datetime`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `zlib`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/utils/GlobalContextCore.improvements.md

# Improvements for GlobalContextCore

**File**: `src\logic\agents\cognitive\context\utils\GlobalContextCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 85 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GlobalContextCore_test.py` with pytest tests

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

from typing import Dict, List, Any, Optional
from datetime import datetime


class GlobalContextCore:
    """
    Pure logic for GlobalContext.
    Handles data merging, pruning, and summary formatting.
    No I/O or direct disk access.
    """

    def partition_memory(
        self, memory: Dict[str, Any], max_entries_per_shard: int = 1000
    ) -> Dict[str, Dict[str, Any]]:
        """
        Splits memory into shards if it exceeds thresholds.
        Implements stable sub-sharding for trillion-parameter scalability (Phase 104).
        """
        import zlib

        shards: Dict[str, Dict[str, Any]] = {"default": {}}
        for category, data in memory.items():
            if isinstance(data, dict):
                if len(data) > max_entries_per_shard:
                    # Logic for Sub-sharding (Stable Hash-based)
                    num_sub_shards = (len(data) // max_entries_per_shard) + 1
                    for key, val in data.items():
                        # Stable hash assignment
                        bucket = zlib.adler32(key.encode()) % num_sub_shards
                        shard_name = f"{category}_{bucket}"
                        if shard_name not in shards:
                            shards[shard_name] = {}
                        shards[shard_name][key] = val
                else:
                    shards["default"][category] = data
            else:
                shards["default"][category] = data
        return shards

    def prepare_fact(self, key: str, value: Any) -> Dict[str, Any]:
        """Prepares a fact entry with timestamp."""
        return {"value": value, "updated_at": datetime.now().isoformat()}

    def prepare_insight(self, insight: str, source_agent: str) -> Dict[str, Any]:
        """Prepares an insight entry."""
        return {
            "text": insight,
            "source": source_agent,
            "timestamp": datetime.now().isoformat(),
        }

    def merge_entity_info(
        self, existing: Dict[str, Any], new_attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merges new attributes into an entity record."""
        updated = existing.copy()
        updated.update(new_attributes)
        updated["last_modified"] = datetime.now().isoformat()
        return updated

    def prune_lessons(
        self, lessons: List[Dict[str, Any]], max_lessons: int = 20
    ) -> List[Dict[str, Any]]:
        """Prunes lessons to keep only the most recent."""
        return lessons[-max_lessons:]

    def generate_markdown_summary(self, memory: Dict[str, Any]) -> str:
        """Logic for formatting the cognitive summary."""
        summary = ["# 🧠 Long-Term Memory Summary"]

        if memory.get("facts"):
            summary.append("\n## 📋 Project Facts")
            for k, v in memory["facts"].items():
                summary.append(f"- **{k}**: {v['value']}")

        if memory.get("constraints"):
            summary.append("\n## ⚠️ Constraints")
            for c in memory["constraints"]:
                summary.append(f"- {c}")

        if memory.get("insights"):
            summary.append("\n## 💡 Key Insights")
            for i in memory["insights"][-5:]:  # Show last 5
                summary.append(f"- {i['text']} (via {i['source']})")

        if memory.get("lessons_learned"):
            summary.append("\n## 🎓 Lessons Learned")
            for l in memory["lessons_learned"][-3:]:
                summary.append(
                    f"- **Issue**: {l['failure']} | **Fix**: {l['correction']}"
                )

        return "\n".join(summary)
