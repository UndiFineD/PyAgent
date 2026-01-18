# SPDX-License-Identifier: Apache-2.0
import numpy as np
from .Config import AttentionConfig
from .Storage import PagedKVCache

class PagedAttentionOps:
    """Pure NumPy implementation of paged attention operations."""
    
    @staticmethod
    def scaled_dot_product_attention(query: np.ndarray, key: np.ndarray, value: np.ndarray, scale: float = 1.0, causal: bool = True, sliding_window: int | None = None) -> np.ndarray:
        scores = np.einsum("bhqd,bhkd->bhqk", query, key) * scale
        sq, sk = query.shape[2], key.shape[2]
        if causal:
            mask = np.triu(np.ones((sq, sk), dtype=bool), k=1)
            scores = np.where(mask, float("-inf"), scores)
        if sliding_window is not None:
            for i in range(sq):
                for j in range(sk):
                    if j < i - sliding_window: scores[:, :, i, j] = float("-inf")
        scores_max = np.max(scores, axis=-1, keepdims=True)
        scores_exp = np.exp(scores - scores_max)
        attn_weights = scores_exp / (np.sum(scores_exp, axis=-1, keepdims=True) + 1e-9)
        return np.einsum("bhqk,bhkd->bhqd", attn_weights, value)
    
    @staticmethod
    def paged_attention_v1(query: np.ndarray, key_cache: PagedKVCache, block_tables: np.ndarray, seq_lens: np.ndarray, config: AttentionConfig) -> np.ndarray:
        num_seqs, num_heads, head_size = query.shape
        output = np.zeros((num_seqs, num_heads, head_size), dtype=query.dtype)
        for seq_idx in range(num_seqs):
            seq_len = seq_lens[seq_idx]
            if seq_len == 0: continue
            valid_blocks = [b for b in block_tables[seq_idx] if b >= 0]
            keys, values = key_cache.read_blocks(valid_blocks, seq_len)
            if config.is_gqa:
                keys = PagedAttentionOps.expand_kv_for_gqa(keys, config.num_queries_per_kv)
                values = PagedAttentionOps.expand_kv_for_gqa(values, config.num_queries_per_kv)
            q = query[seq_idx:seq_idx+1].reshape(1, num_heads, 1, head_size)
            k = keys.reshape(1, num_heads, seq_len, head_size)
            v = values.reshape(1, num_heads, seq_len, head_size)
            out = PagedAttentionOps.scaled_dot_product_attention(q, k, v, scale=config.scale, causal=True, sliding_window=config.sliding_window)
            output[seq_idx] = out.reshape(num_heads, head_size)
        return output
    
    @staticmethod
    def paged_attention_v2(query: np.ndarray, key_cache: PagedKVCache, block_tables: np.ndarray, seq_lens: np.ndarray, config: AttentionConfig, partition_size: int = 512) -> np.ndarray:
        ns, nh, hs = query.shape
        output = np.zeros((ns, nh, hs), dtype=query.dtype)
        for seq_idx in range(ns):
            sl = seq_lens[seq_idx]
            if sl == 0: continue
            keys, values = key_cache.read_blocks([b for b in block_tables[seq_idx] if b >= 0], sl)
            if config.is_gqa:
                keys = PagedAttentionOps.expand_kv_for_gqa(keys, config.num_queries_per_kv)
                values = PagedAttentionOps.expand_kv_for_gqa(values, config.num_queries_per_kv)
            num_parts = (sl + partition_size - 1) // partition_size
            exps, maxs, part_out = np.zeros(nh), np.full(nh, float("-inf")), np.zeros((nh, hs))
            q = query[seq_idx]
            for pi in range(num_parts):
                s, e = pi * partition_size, min((pi + 1) * partition_size, sl)
                scores = np.einsum("hd,phd->hp", q, keys[s:e]) * config.scale
                p_max = np.max(scores, axis=1)
                new_max = np.maximum(maxs, p_max)
                old_s = np.exp(maxs - new_max)
                exps, part_out = exps * old_s, part_out * old_s[:, None]
                e_scores = np.exp(scores - new_max[:, None])
                exps += np.sum(e_scores, axis=1)
                part_out += np.einsum("hp,phd->hd", e_scores, values[s:e])
                maxs = new_max
            output[seq_idx] = part_out / (exps[:, None] + 1e-9)
        return output.astype(query.dtype)
    
    @staticmethod
    def expand_kv_for_gqa(kv: np.ndarray, nq_per_kv: int) -> np.ndarray:
        return kv if nq_per_kv == 1 else np.repeat(kv, nq_per_kv, axis=1)
