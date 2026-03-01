# Storage

**File**: `src\infrastructure\attention\paged_attention\Storage.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 6 imports  
**Lines**: 142  
**Complexity**: 16 (moderate)

## Overview

Python module containing implementation for Storage.

## Classes (4)

### `BlockTable`

Manages physical block allocation for sequences.

**Methods** (6):
- `__post_init__(self)`
- `allocate_block(self, seq_id)`
- `free_sequence(self, seq_id)`
- `get_block_table(self, seq_id)`
- `num_allocated_blocks(self, seq_id)`
- `num_free_blocks(self)`

### `SlotMapping`

Maps tokens to (block_idx, block_offset) slots.

**Methods** (3):
- `compute_slot(self, block_idx, offset)`
- `decode_slot(self, slot)`
- `map_sequence_slots(self, block_table, seq_len)`

### `PagedKVCache`

Block-organized key/value cache.

**Methods** (4):
- `__post_init__(self)`
- `write(self, key, value, slot_mapping)`
- `read_blocks(self, block_table, seq_len)`
- `get_memory_usage(self)`

### `AttentionMetadata`

Metadata for batched attention computation.

**Methods** (3):
- `num_seqs(self)`
- `total_tokens(self)`
- `from_seq_lens(cls, seq_lens, block_tables, block_size, max_blocks_per_seq)`

## Dependencies

**Imports** (6):
- `Config.AttentionConfig`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `numpy`
- `typing.Sequence`

---
*Auto-generated documentation*
