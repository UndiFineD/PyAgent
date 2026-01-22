# PyAgent Rust Mapping Strategy

This document outlines the performance-critical "Hot Paths" identified for migration to `rust_core` (FFI). 

## 1. High-Throughput Logic (The "Hot Paths")

| Component | Target Function | Reason |
|-----------|-----------------|---------|
| **LoRA Management** | `merge_weights`, `apply_adapter` | Heavy linear algebra (Add/Mul) on large tensors. |
| **Logic/Pruning** | `calculate_decay`, `calculate_weights` | Recursive calculations across large agent graphs. |
| **Common/Metrics**| `aggregate_metrics`, `rolling_avg` | Processing thousands of metric points per second. |
| **Common/Telemetry**| `calculate_rollups`, `percentiles` | Fast bucketing and statistics across massive telemetry streams. |
| **Swarm/Auction** | `calculate_vcg_prices` | Combinatorial optimization in large-scale bidding. |
| **Storage/Cache** | `generate_hash`, `verify_integrity` | Bulk byte processing and cryptographic hashing (MD5/SHA). |
| **Inference/KV**  | `page_copy`, `block_manager` | Low-level memory management and pointer arithmetic for paged attention. |
| **Common/Template**| `apply_template` | Fast regex and string substitution for massive prompt batches. |
| **Common/Config**  | `load_config`, `_parse` | High-speed parsing of multi-GB configuration sharded files. |
| **Common/Registry**| `detect_cycles`, `topo_sort` | Complex graph analysis for agent dependency resolution. |
| **Common/Validation**| `json_schema_validate` | High-speed schema checking for structured model output. |
| **Common/Memory**  | `search_vector_rust` | Vector similarity/search for agent long-term memory. || **Common/Search**  | `find_literal_rust` | Fast substring/regex search across thousands of files. |
| **Common/Analysis**| `calculate_complexity_rust` | Fast cyclomatic complexity calculation during agent linting. |
| **Common/Validation**| `validate_content_rust` | Fast regex/string matching for security and content safety. |
| **Common/Inference** | `apply_lora_rust` | Linear algebra (MatMul) for high-speed dynamic adapter merging. |
| **Common/Inference** | `count_tokens_rust` | Native Llama/Gpt tokenizer implementations (speed). |
| **Common/Connectivity**| `establish_native_rust` | High-throughput binary framing and multiplexing. |
## 2. Global Protocol Support

Rust should be used for the underlying implementation of:
- **`BaseCore.save_atomic()`**: Ensuring transactional speed and safety when writing large state files.
- **`ConnectivityCore.binary_transport`**: High-speed serialization (MessagePack/Zstd) and network I/O.
- **`KnowledgeCore.sharding_index`**: Fast bucket distribution using Adler-32.

## 3. Current Implementation Status

`src/core/base/common/` entities are already pre-wired with `try: import rust_core as rc` blocks to support graceful fallback.

### Completed Hooks:
- [x] `CacheCore`: MD5 hashing.
- [x] `PriorityCore`: Weight calculation.
- [x] `AuctionCore`: Pricing algorithms.
- [x] `PruningCore`: Synaptic decay math.
- [x] `ConnectivityCore`: Connection establishment.

### Next Priority for Rust:
1. **LoRA Adapter Merging**: Migrating `src/infrastructure/engine/adapters/lora/` math to Rust.
2. **Bulk FS Operations**: Migrating `src/core/base/common/file_system_core.py` directory scanning and hashing.
