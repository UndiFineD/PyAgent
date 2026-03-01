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
