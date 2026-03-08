# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/core_mixins/CorePartitionMixin.description.md

# CorePartitionMixin

**File**: `src\logic\agents\cognitive\context\engines\core_mixins\CorePartitionMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 74  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for CorePartitionMixin.

## Classes (1)

### `CorePartitionMixin`

Methods for partitioning and bloat detection.

**Methods** (2):
- `partition_memory(self, memory, max_entries_per_shard)`
- `detect_shard_bloat(self, shards, size_threshold_bytes)`

## Dependencies

**Imports** (5):
- `json`
- `rust_core.partition_to_shards_rust`
- `typing.Any`
- `zlib`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/core_mixins/CorePartitionMixin.improvements.md

# Improvements for CorePartitionMixin

**File**: `src\logic\agents\cognitive\context\engines\core_mixins\CorePartitionMixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 74 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CorePartitionMixin_test.py` with pytest tests

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

from typing import Any
import json

try:
    from rust_core import partition_to_shards_rust

    _RUST_ACCEL = True
except ImportError:
    _RUST_ACCEL = False


class CorePartitionMixin:
    """Methods for partitioning and bloat detection."""

    def partition_memory(
        self, memory: dict[str, Any], max_entries_per_shard: int = 1000
    ) -> dict[str, dict[str, Any]]:
        """
        Splits memory into shards if it exceeds thresholds.
        Implements stable sub-sharding for trillion-parameter scalability.
        """
        import zlib

        shards: dict[str, dict[str, Any]] = {"default": {}}
        for category, data in memory.items():
            if not isinstance(data, dict) or not data:
                shards["default"][category] = data
                continue

            count = len(data)
            if count > max_entries_per_shard:
                # Use Rust for sharding if available
                if _RUST_ACCEL:
                    try:
                        items = [(k, json.dumps(v)) for k, v in data.items()]
                        rust_shards = partition_to_shards_rust(
                            category, items, max_entries_per_shard
                        )
                        for shard_name, shard_items in rust_shards:
                            if shard_name not in shards:
                                shards[shard_name] = {}
                            for key, val_json in shard_items:
                                shards[shard_name][key] = json.loads(val_json)
                        continue
                    except Exception:
                        pass  # Fall through to Python

                # Python fallback: Sub-sharding (Stable Hash-based)
                num_sub_shards = 2 ** ((count // max_entries_per_shard).bit_length())

                for key, val in data.items():
                    # Adler-32 is fast and sufficient for non-cryptographic sharding
                    hash_input = f"{category}:{key}"
                    bucket = zlib.adler32(hash_input.encode()) % num_sub_shards
                    shard_name = f"{category}_{bucket}"
                    if shard_name not in shards:
                        shards[shard_name] = {}
                    shards[shard_name][key] = val
            else:
                shards["default"][category] = data
        return shards

    def detect_shard_bloat(
        self, shards: dict[str, dict[str, Any]], size_threshold_bytes: int = 5_000_000
    ) -> list[str]:
        """Identifies shards that are exceeding the recommended size."""
        import json

        bloated = []
        for name, data in shards.items():
            # Estimate size via JSON serialization
            size = len(json.dumps(data))
            if size > size_threshold_bytes:
                bloated.append(name)
        return bloated
