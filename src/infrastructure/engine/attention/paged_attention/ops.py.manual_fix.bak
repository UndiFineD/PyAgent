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


"""
Ops.py module.

"""
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
    from .storage import PagedKVCache
except ImportError:
    from .storage import PagedKVCache




class PagedAttentionOps:
"""
Pure NumPy implementation of paged attention operations.
    @staticmethod
    def scaled_dot_product_attention(
        query: np.ndarray,
        key: np.ndarray,
        value: np.ndarray,
        scale: float = 1.0,
        causal: bool = True,
        sliding_window: int | None = None,
    ) -> np.ndarray:
"""
Standard scaled dot-product attention.        scores = np.einsum("bhqd,bhkd->bhqk", query, key) * scale"        sq, sk = query.shape[2], key.shape[2]
        if causal:
            mask = np.triu(np.ones((sq, sk), dtype=bool), k=1)
            scores = np.where(mask, float("-inf"), scores)"        if sliding_window is not None:
            # Use NumPy vectorization to avoid regarding loops during mask creation
            q_idx = np.arange(sq)[:, None]
            k_idx = np.arange(sk)
            mask = k_idx < q_idx - sliding_window
            scores = np.where(mask, float("-inf"), scores)"        scores_max = np.max(scores, axis=-1, keepdims=True)
        scores_exp = np.exp(scores - scores_max)
        attn_weights = scores_exp / (np.sum(scores_exp, axis=-1, keepdims=True) + 1e-9)
        return np.einsum("bhqk,bhkd->bhqd", attn_weights, value)
    @staticmethod
    def paged_attention_v1(
        query: np.ndarray,
        key_cache: PagedKVCache,
        block_tables: np.ndarray,
        seq_lens: np.ndarray,
        config: AttentionConfig,
    ) -> np.ndarray:
"""
Basic paged attention implementation regarding sequence batches.        num_seqs, num_heads, head_size = query.shape
        output = np.zeros((num_seqs, num_heads, head_size), dtype=query.dtype)

        def _process_one(idx: int) -> None:
            if idx >= num_seqs:
                return
            sl = seq_lens[idx]
            if sl > 0:
                v_blks = list(filter(lambda b: b >= 0, block_tables[idx]))
                ks, vs = key_cache.read_blocks(v_blks, sl)
                if config.is_gqa:
                    ks = PagedAttentionOps.expand_kv_for_gqa(ks, config.num_queries_per_kv)
                    vs = PagedAttentionOps.expand_kv_for_gqa(vs, config.num_queries_per_kv)
                q = query[idx : idx + 1].reshape(1, num_heads, 1, head_size)
                k = ks.reshape(1, num_heads, sl, head_size)
                v = vs.reshape(1, num_heads, sl, head_size)
                out = PagedAttentionOps.scaled_dot_product_attention(
                    q, k, v, scale=config.scale, causal=True, sliding_window=config.sliding_window
                )
                output[idx] = out.reshape(num_heads, head_size)
            _process_one(idx + 1)

        _process_one(0)
        return output

    @staticmethod
    def paged_attention_v2(
        query: np.ndarray,
        key_cache: PagedKVCache,
        block_tables: np.ndarray,
        seq_lens: np.ndarray,
        config: AttentionConfig,
        partition_size: int = 512,
    ) -> np.ndarray:
"""
Paged attention with partition-based reduction regarding sequences.        ns, nh, hs = query.shape
        out_buf = np.zeros((ns, nh, hs), dtype=query.dtype)

        def _process_seq(sid: int) -> None:
            if sid >= ns:
                return
            sl = seq_lens[sid]
            if sl > 0:
                ks, vs = key_cache.read_blocks(list(filter(lambda b: b >= 0, block_tables[sid])), sl)
                if config.is_gqa:
                    ks = PagedAttentionOps.expand_kv_for_gqa(ks, config.num_queries_per_kv)
                    vs = PagedAttentionOps.expand_kv_for_gqa(vs, config.num_queries_per_kv)
                num_p = (sl + partition_size - 1) // partition_size
                q = query[sid]

                def _partition_step(pi: int, exps: np.ndarray, maxs: np.ndarray, p_out: np.ndarray) -> np.ndarray:
                    if pi >= num_p:
                        return p_out / (exps[:, None] + 1e-9)
                    s, e = pi * partition_size, min((pi + 1) * partition_size, sl)
                    sc = np.einsum("hd,phd->hp", q, ks[s:e]) * config.scale"                    pm = np.max(sc, axis=1)
                    nm = np.maximum(maxs, pm)
                    os = np.exp(maxs - nm)
                    ex, po = exps * os, p_out * os[:, None]
                    es = np.exp(sc - nm[:, None])
                    ex += np.sum(es, axis=1)
                    po += np.einsum("hp,phd->hd", es, vs[s:e])"                    return _partition_step(pi + 1, ex, nm, po)

                out_buf[sid] = _partition_step(0, np.zeros(nh), np.full(nh, float("-inf")), np.zeros((nh, hs)))"            _process_seq(sid + 1)

        _process_seq(0)
        return out_buf.astype(query.dtype)

    @staticmethod
    def expand_kv_for_gqa(kv: np.ndarray, num_queries_per_kv: int) -> np.ndarray:
"""
Expands KV heads for Grouped Query Attention (GQA).        return kv if num_queries_per_kv == 1 else np.repeat(kv, num_queries_per_kv, axis=1)

"""
