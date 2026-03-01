# AttentionBufferAgent

**File**: `src\classes\specialized\AttentionBufferAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 123  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for AttentionBufferAgent.

## Classes (1)

### `AttentionBufferAgent`

**Inherits from**: BaseAgent

Tier 2 (Cognitive Logic) - Attention Buffer Agent: Maintains a shared 
attention context between humans and agents to ensure cohesive collaboration.

Phase 14 Rust Optimizations:
- sort_buffer_by_priority_rust: Fast priority-timestamp composite sorting
- filter_stale_entries_rust: Optimized timestamp-based filtering

**Methods** (4):
- `__init__(self, file_path)`
- `push_attention_point(self, source, content, priority)`
- `get_attention_summary(self)`
- `clear_stale_attention(self, age_seconds)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `rust_core`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
