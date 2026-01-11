# Data Structures & Knowledge Architecture (Jan 2026)

## Overview
To support trillion-parameter scaling and multi-agent coordination, we have implemented a sharded, isolated knowledge architecture. Data is stored per agent in a 3-tier "Knowledge Trinity" (B-Tree, Vector, Graph).

## 1. Per-Agent Isolation
Each agent has a dedicated directory in `data/agents/{agent_id}/`.
- `structured/`: Sharded B-Tree (JSON) for deterministic facts.
- `semantic/`: Vector Store (ChromaDB) for similarity-based memory.
- `relational/`: Knowledge Graph (Triples) for causal and ontological links.

## 2. Trillion-Parameter Scaling (Phase 123-126)
### A. Hierarchical B-Tree Sharding
We use a 2-tier MD5-based sharding strategy to prevent filesystem directory saturation:
`data/agents/{id}/structured/{hash[:2]}/{hash[2:4]}/{key}.json`
This allows for trillions of keys while keeping lookups at $O(1)$ relative to the filesystem.

### B. High-Throughput Context Recording (Trace Sharding)
Interaction logs in `data/logs/external_ai_learning/` use a monthly + hash-based sharding strategy:
`shard_{YYYYMM}_{000-255}.jsonl.gz`
This ensures that trillion-parameter datasets can be harvested in parallel without lock contention on single files. We use GZIP compression to reduce storage footprint by ~75%.

**Performance Optimization (Phase 128)**: A Rust-based `fast_hash` (PyO3) hook is implemented in `btree_store.py` to accelerate shard path generation, achieving sub-millisecond page targeting during high-frequency writes.

### B. Dynamic Vector Quantization
Semantic memory uses quantized embeddings to minimize storage footprint. The `VectorKnowledgeStore` supports local HNSW indices for sub-millisecond similarity search across millions of records per agent.
Each agent's vector store is isolated in `data/agents/{id}/semantic/`.

### C. Ontological Graph Pruning
The `GraphKnowledgeStore` tracks S-P-O triples. We implement a `KnowledgePruningEngine` (refactored from `NeuralPruningEngine`) that evicts weak or non-reinforced relationships during "Sleep" cycles, maintaining a high signal-to-noise ratio in the agent's long-term graph memory.

#### Anchoring Strength & Utility Decay
Pruning decisions are governed by a time-decayed utility score called **Anchoring Strength** ($S$):
$$S = C \cdot e^{-k \Delta t}$$
Where:
- $C$: Initial utility or "Anchoring Count" (hits/accesses).
- $k$: Decay constant (sensitivity to time).
- $\Delta t$: Time elapsed since last access.

The engine (implemented in `src/core/knowledge/knowledge_pruning_engine.py`) performs periodic sweeps, evicting knowledge nodes where $S < \tau$ (threshold). This ensures the agent's memory prioritizes recent and frequently reinforced facts.

The graph is persisted per agent in `data/agents/{id}/relational/`.


### D. Phase 128: Dynamic Communication Sharding
To further optimize swarm latency, we implement dynamic sharding based on agent interaction frequency.
- **Telemetry-informed clustering**: Shards are restructured every 1000 interactions to cluster agents that communicate frequently.
- **Latency reduction**: By placing frequently interacting agents in the same logical shard, we reduce the overhead of inter-shard synchronization.
- **Isolation Enforcement**: While shards are logical clusters for performance, the Knowledge Trinity (B-Tree, Vector, Graph) remains physically siloed per agent to ensure privacy and prevent representation collapse.

## 3. The Knowledge Trinity Access Patterns
1. **Direct Lookup (B-Tree)**: "What is the exact CRC of file X?"
2. **Associative Search (Vector)**: "Have we seen a bug similar to this before?"
3. **Causal Reasoning (Graph)**: "If we change module A, which specialized agents might be affected?"

## 4. Stability & Privacy
- **Differential Privacy**: Applied at the B-Tree serialization layer to strip PII.
- **Circuit Breakers**: Knowledge retrieval is wrapped in circuit breakers to prevent swarm deadlock if a storage node becomes unresponsive.
