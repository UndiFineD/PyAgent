#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Engine.py module.

try:
    from typing import Dict, List
except ImportError:
    from typing import Dict, List


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .config import AttentionConfig
except ImportError:
    from .config import AttentionConfig

try:
    from .enums import KVCacheDtype
except ImportError:
    from .enums import KVCacheDtype

try:
    from .ops import PagedAttentionOps
except ImportError:
    from .ops import PagedAttentionOps

try:
    from .storage import BlockTable, PagedKVCache, SlotMapping
except ImportError:
    from .storage import BlockTable, PagedKVCache, SlotMapping




class PagedAttentionEngine:
        Engine for managing paged KV cache and executing paged attention operations.
        def __init__(self, config: AttentionConfig, num_blocks: int = 1024) -> None:
        """Initializes the paged attention engine.        self.config = config
        self.block_table = BlockTable(num_blocks, config.block_size)
        dtype = np.float16 if config.kv_cache_dtype == KVCacheDtype.FP16 else np.float32
        self.kv_cache = PagedKVCache(num_blocks, config.block_size, config.num_kv_heads, config.head_size, dtype)
        self.slot_mapper = SlotMapping(config.block_size)
        self._seq_positions: Dict[int, int] = {}

    def allocate_sequence(self, seq_id: int, initial_len: int = 0) -> None:
        """Allocates blocks for a new sequence.        if seq_id in self.block_table.block_tables:
            return
        nb = (initial_len + self.config.block_size - 1) // self.config.block_size
        for _ in range(max(1, nb)):
            self.block_table.allocate_block(seq_id)
        self._seq_positions[seq_id] = initial_len

    def append_kv(self, seq_id: int, key: np.ndarray, value: np.ndarray) -> None:
        """Appends KV pairs for a sequence to the cache.        nt = key.shape[0]
        cp = self._seq_positions.get(seq_id, 0)
        rb = (cp + nt + self.config.block_size - 1) // self.config.block_size
        cb = self.block_table.num_allocated_blocks(seq_id)
        while cb < rb:
            self.block_table.allocate_block(seq_id)
            cb += 1
        bt = self.block_table.get_block_table(seq_id)
        slots = np.zeros(nt, dtype=np.int64)
        for i in range(nt):
            tp = cp + i
            bi, off = divmod(tp, self.config.block_size)
            slots[i] = self.slot_mapper.compute_slot(bt[bi], off)
        self.kv_cache.write(key, value, slots)
        self._seq_positions[seq_id] = cp + nt

    def forward(self, query: np.ndarray, seq_ids: List[int], use_v2: bool = True) -> np.ndarray:
        """Performs paged attention forward pass.        sl = np.array([self._seq_positions.get(sid, 0) for sid in seq_ids], dtype=np.int32)
        mb = max((self.block_table.num_allocated_blocks(sid) for sid in seq_ids), default=1)
        bt = np.full((len(seq_ids), mb), -1, dtype=np.int32)
        for i, sid in enumerate(seq_ids):
            tbl = self.block_table.get_block_table(sid)
            for j, b in enumerate(tbl[:mb]):
                bt[i, j] = b
        if use_v2:
            return PagedAttentionOps.paged_attention_v2(query, self.kv_cache, bt, sl, self.config)
        return PagedAttentionOps.paged_attention_v1(query, self.kv_cache, bt, sl, self.config)

    def free_sequence(self, seq_id: int) -> None:
        """Frees blocks allocated for a sequence.        self.block_table.free_sequence(seq_id)
        self._seq_positions.pop(seq_id, None)

    def get_stats(self) -> dict:
        """Returns cache and engine statistics.        return {
            "num_sequences": len(self._seq_positions),"            "num_allocated_blocks": self.block_table.num_blocks - self.block_table.num_free_blocks,"            "num_free_blocks": self.block_table.num_free_blocks,"            "kv_cache_memory_mb": self.kv_cache.get_memory_usage() / (1024 * 1024),"        }


def create_attention_engine(
    head_size: int = 64,
    num_heads: int = 32,
    num_kv_heads: int = 8,
    block_size: int = 16,
    num_blocks: int = 1024,
) -> PagedAttentionEngine:
    """Utility function to create a PagedAttentionEngine with default config.    config = AttentionConfig(
        head_size=head_size,
        num_heads=num_heads,
        num_kv_heads=num_kv_heads,
        block_size=block_size
    )
    return PagedAttentionEngine(config, num_blocks)
