# Rust Acceleration Roadmap (Phase 40+)

PyAgent uses a high-performance Rust core (`rust_core`) to offload CPU-intensive tasks from the Python event loop. This enables the swarm to scale to thousands of tokens per second and maintain low latency in complex orchestrations.

## Current Hot Paths (Rust Integrated)

1.  **Metric Calculation** (`calculate_token_cost`): Handles fast pricing lookups and aggregations.
2.  **Episodic Memory Ranking** (`rank_memories_rust`): Sorts and filters thousands of memories using utility scores.
3.  **FAST-Hash** (`fast_hash`): Used for sub-millisecond page access in Sharded B-Trees.
4.  **Logprob Analytics** (`compute_perplexity_rust`, `compute_entropy_rust`): Statistical analysis of model outputs.

## Prioritized Hot Paths (Rust Migration Pending)

| Category | Component | Why Rust? |
|:---|:---|:---|
| **Formula Evaluation** | `FormulaCore.evaluate` | Evaluating nested AST math expressions for large-scale telemetry is O(N) in Python. Rust can use a static parser. |
| **Bulk I/O Serialization** | `StorageCore.to_json` | Large state files (e.g., `agent_knowledge_index.json` > 50MB) block the event loop during serialization. |
| **Code Analysis** | `AnalysisCore.get_imports` | Scanning thousands of files for dependencies during swarm updates. |
| **Bulk Replacement** | `base_utilities.bulk_replace` | Multi-file regex/string replacements (Phase 318 Parallel Engine). |
| **Telemetry Aggregation** | `MetricsEngine` | Rolling up thousands of events per second into hourly/daily shards. |

## Integration Strategy

1.  **Bridge via PyO3**: All Rust functions must be exposed via `rust_core` and wrapped in their respective Python `*Core` classes.
2.  **Python Fallback**: Every Rust-accelerated method MUST have a pure-Python fallback to ensure portability.
3.  **Memory Safety**: Leverage Rust's ownership model for shared buffers (Zero-copy) when processing large model weights or context caches.
