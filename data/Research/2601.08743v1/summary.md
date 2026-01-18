# TableCache: Hierarchical KV Cache Precomputation for Low Latency Text-to-SQL
**arXiv ID**: 2601.08743
**Date**: January 13, 2026
**Authors**: NVIDIA Research

## Summary
TableCache optimizes Text-to-SQL tasks by precomputing and caching the structural metadata of databases as hierarchical KV caches. It uses a "Table Trie" structure to quickly retrieve the relevant structural "thoughts" during the prefill phase, significantly reducing Time to First Token (TTFT).

## Key Innovations
1.  **Hierarchical KV Caching**: Instead of a flat prompt containing table schemas, it tiles the schema into hierarchical blocks.
2.  **Table Trie**: A retrieval-augmented trie that matches query keywords to precomputed KV cache segments.
3.  **Hot-Swapping**: Injects cached table representations directly into the model's KV cache window without re-processing.

## Performance
-   **3.62x speedup** in TTFT for complex multi-table joins.
-   Reduces redundant schema processing tokens by up to 90%.

## Implementation Details for PyAgent
-   **Integration Point**: `src/infrastructure/engine/kv_cache/RadixTreeManager.py`.
-   **Mechanism**:
    -   Store table schemas in a dedicated KV cache repository.
    -   When a tool call or SQL query is detected, look up the table IDs in the Trie.
    -   Stitch the cached table KV fragments into the current request's prompt prefix.
