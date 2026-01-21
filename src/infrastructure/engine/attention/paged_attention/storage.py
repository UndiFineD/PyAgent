# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence
import numpy as np
from .config import AttentionConfig

@dataclass
class BlockTable:
    """Manages physical block allocation for sequences."""
    num_blocks: int
    block_size: int
    block_tables: dict[int, list[int]] = field(default_factory=dict)
    free_blocks: set[int] = field(default_factory=set)
    
    def __post_init__(self):
        self.free_blocks = set(range(self.num_blocks))
    
    def allocate_block(self, seq_id: int) -> int:
        if not self.free_blocks: raise RuntimeError("No free blocks available")
        block_idx = self.free_blocks.pop()
        if seq_id not in self.block_tables: self.block_tables[seq_id] = []
        self.block_tables[seq_id].append(block_idx)
        return block_idx
    
    def free_sequence(self, seq_id: int) -> list[int]:
        if seq_id not in self.block_tables: return []
        freed = self.block_tables.pop(seq_id)
        self.free_blocks.update(freed)
        return freed
    
    def get_block_table(self, seq_id: int) -> list[int]:
        return self.block_tables.get(seq_id, [])
    
    def num_allocated_blocks(self, seq_id: int) -> int:
        return len(self.block_tables.get(seq_id, []))
    
    @property
    def num_free_blocks(self) -> int: return len(self.free_blocks)


@dataclass
class SlotMapping:
    """Maps tokens to (block_idx, block_offset) slots."""
    block_size: int
    slots: np.ndarray = field(default_factory=lambda: np.array([], dtype=np.int64))
    
    def compute_slot(self, block_idx: int, offset: int) -> int:
        return block_idx * self.block_size + offset
    
    def decode_slot(self, slot: int) -> tuple[int, int]:
        """Decode slot into (block_idx, block_offset)."""
        return divmod(slot, self.block_size)
    
    def map_sequence_slots(self, block_table: list[int], seq_len: int) -> np.ndarray:
        slots = np.zeros(seq_len, dtype=np.int64)
        for i in range(seq_len):
            block_idx = i // self.block_size
            offset = i % self.block_size
            if block_idx < len(block_table):
                slots[i] = self.compute_slot(block_table[block_idx], offset)
            else: slots[i] = -1
        return slots


@dataclass
class PagedKVCache:
    """Block-organized key/value cache."""
    num_blocks: int
    block_size: int
    num_kv_heads: int
    head_size: int
    dtype: np.dtype = np.float32
    key_cache: np.ndarray | None = field(default=None, repr=False)
    value_cache: np.ndarray | None = field(default=None, repr=False)
    
    def __post_init__(self):
        shape = (self.num_blocks, self.block_size, self.num_kv_heads, self.head_size)
        self.key_cache = np.zeros(shape, dtype=self.dtype)
        self.value_cache = np.zeros(shape, dtype=self.dtype)
    
    def write(self, key: np.ndarray, value: np.ndarray, slot_mapping: np.ndarray) -> None:
        for i, slot in enumerate(slot_mapping):
            if slot < 0: continue
            block_idx, offset = divmod(slot, self.block_size)
            self.key_cache[block_idx, offset] = key[i]
            self.value_cache[block_idx, offset] = value[i]
    
    def read_blocks(self, block_table: list[int], seq_len: int) -> tuple[np.ndarray, np.ndarray]:
        keys = np.zeros((seq_len, self.num_kv_heads, self.head_size), dtype=self.dtype)
        values = np.zeros((seq_len, self.num_kv_heads, self.head_size), dtype=self.dtype)
        for i in range(seq_len):
            block_idx, offset = divmod(i, self.block_size)
            if block_idx < len(block_table):
                phys_block = block_table[block_idx]
                keys[i] = self.key_cache[phys_block, offset]
                values[i] = self.value_cache[phys_block, offset]
        return keys, values
    
    def get_memory_usage(self) -> int:
        return (self.key_cache.nbytes + self.value_cache.nbytes) if self.key_cache is not None else 0


@dataclass
class AttentionMetadata:
    """Metadata for batched attention computation."""
    seq_lens: np.ndarray
    query_start_loc: np.ndarray
    max_query_len: int
    max_seq_len: int
    block_tables: np.ndarray
    slot_mapping: np.ndarray
    num_prefill_tokens: int = 0
    num_decode_tokens: int = 0
    
    @property
    def num_seqs(self) -> int: return len(self.seq_lens)
    @property
    def total_tokens(self) -> int: return int(np.sum(self.seq_lens))
    
    @classmethod
    def from_seq_lens(cls, seq_lens: Sequence[int], block_tables: list[list[int]], block_size: int, max_blocks_per_seq: int) -> "AttentionMetadata":
        seq_lens_arr = np.array(seq_lens, dtype=np.int32)
        query_start_loc = np.zeros(len(seq_lens) + 1, dtype=np.int32)
        query_start_loc[1:] = np.cumsum(seq_lens_arr)
        
        block_tables_arr = np.full((len(seq_lens), max_blocks_per_seq), -1, dtype=np.int32)
        for i, table in enumerate(block_tables):
            for j, block in enumerate(table[:max_blocks_per_seq]):
                block_tables_arr[i, j] = block
        
        total_tokens = int(np.sum(seq_lens_arr))
        slot_mapping = np.zeros(total_tokens, dtype=np.int64)
        slot_mapper = SlotMapping(block_size)
        token_idx = 0
        for seq_idx, seq_len in enumerate(seq_lens):
            seq_slots = slot_mapper.map_sequence_slots(block_tables[seq_idx], seq_len)
            slot_mapping[token_idx:token_idx + seq_len] = seq_slots
            token_idx += seq_len
        
        return cls(seq_lens=seq_lens_arr, query_start_loc=query_start_loc, max_query_len=max(seq_lens, default=0),
                   max_seq_len=max(seq_lens, default=0), block_tables=block_tables_arr, slot_mapping=slot_mapping)
