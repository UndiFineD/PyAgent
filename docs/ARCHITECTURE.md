# PyAgent: 319-Phase Swarm Architecture (VOYAGER STABILITY)

## Overview
PyAgent has evolved from a single-agent orchestrator into a multi-agent swarm capable of autonomous, secure, and transactionally safe self-improvement. Following the **Phase 319 (Voyager Stability)** milestone, the system now features a decentralized peer-to-peer transport layer and enhanced Rust-native metrics.

## Core Architectural Pillars

### 1. Rust Bridge & Acceleration (`rust_core/`)
The primary performance layer is now a Rust-based FFI bridge (`rust_core.pyd`).
- **41% Acceleration**: CPU-bound tasks like cyclomatic complexity calculation, pattern matching, and JSON logging are delegated to Rust.
- **CodeHealth Guard**: Phase 319 introduces Rust-native metrics (C901, MI) in `CodeHealthAuditor`, enabling latency-free workspace audits (< 5ms per file).
- **Parallel Bulk Replace**: High-throughput file modification engine implemented in Rust to handle workspace-wide refactoring without event loop blockage.

### 2. Voyager Decentralized Transport (`src/infrastructure/voyager/`)
The "Voyager" layer provides a zero-broker, decentralized message bus for multi-node swarms.
- **mDNS Discovery**: Uses `DiscoveryNode` (zeroconf) to advertise node capabilities and transport ports automatically on the local network.
- **ZMQ Neural Synapse**: Implements the DEALER/ROUTER pattern for high-speed, asynchronous task teleportation between fleets.
- **Graceful Stability**: Specialized asyncio handling for Ctrl+C and socket termination ensures 100% clean shutdowns even on Windows (`SelectorEventLoop`).

### 3. Cascade Context and Lineage (`src/core/base/`)
Introduced `CascadeContext` to solve the challenge of thread-safe recursion in complex task delegations. Every task maintains a lineage of its parentage, preventing infinite loops and providing deep observability into the "reasoning chain."

### 2. Fleet Priority & Preemption (`src/infrastructure/fleet/`)
The `FleetManager` and `FleetExecutionCore` now support `AgentPriority` (Low, Standard, High, Critical). 
- **Active Task Registry**: Tracks all running agents and their priorities.
- **Preemption**: When a high-priority task arrives, the Fleet can invoke `suspend()` on lower-priority agents, freeing up LLM bandwidth and compute resources.

### 3. Neural Pruning & Synaptic Decay (`src/core/base/NeuralPruningEngine.py`)
To maintain high-performance sharding, the system implements exponential decay for knowledge paths.
- **50-Cycle Penalty**: Agents or paths that remain idle for more than 50 execution cycles suffer a 50% synaptic weight reduction.
- **Pruning Core**: Automatically removes "forgotten" facts that fall below the efficiency threshold.

### 4. Binary Shard Snapshots (`src/infrastructure/storage/`)
Moving beyond JSON, the system uses `msgpack` and `blake3` for high-speed indexing and binary snapshots.
- **O(1) Lookups**: Localized B-Tree indexing.
- **Snapshots**: Periodic binary dumps of the global knowledge state allow for near-instantaneous restoration of the swarm's memory.

### 5. Secure Asynchronous Execution (`src/core/base/shell.py`)
Shell operations are now fully asynchronous and sandboxed.
- **Environment Sanitizer**: Prevents the leakage of environment variables (keys, secrets) to subprocesses via an allow-list protocol.
- **Real-time Streaming**: Non-blocking `stdout/stderr` capture for live logging.

### 6. Transactional State Integrity (`src/core/base/state.py`)
All file-system modifications are wrapped in `StateTransaction`.
- **Atomic Operations**: Changes are buffered.
- **Rollback**: If an agent fails midway through a multi-file refactor, the `StateTransaction` restores previous states from a secure vault.

### 7. Mixin-Based Agent Modularization (`src/core/base/mixins/`)
Following the Phase 317 complexity sweep, the monolithic `BaseAgent` (Complexity: 135) was refactored into a decentralized Mixin architecture.
- **IdentityMixin**: Handles agent naming, versioning, and core metadata.

### 8. Phase 48: Advanced Memory & API Partitioning (v3.16.x)
To manage extreme complexity and performance in inference sub-systems, major monolithic components were modularized into high-cohesion sub-packages.
- **Paged Attention Engine**: Split into `src/infrastructure/attention/paged_attention/`, implementing partitioned online softmax and block-based KV management.
- **OpenAI Responses API Server**: Modularized into `src/infrastructure/openai_api/responses/`, featuring dedicated models, storage, and SSE streaming handlers.
- **NIXL RDMA Connector**: High-performance KV transfer logic using Rust-accelerated RDMA memory registration and block-wise zero-copy transfers between prefill and decode instances.
- **PersistenceMixin**: Manages state serialization, checkpointing, and history.
- **KnowledgeMixin**: Orchestrates access to the "Knowledge Trinity" (Structured, Semantic, Relational).
- **OrchestrationMixin**: Manages task delegation, tool calling, and recursive reasoning.
- **GovernanceMixin**: Enforces security protocols, privacy boundaries, and ethical guardrails.

## Roadmap: Project "VOYAGER"
- **P2P Swarms (DONE)**: Decentralized fleet synchronization with mDNS discovery.
- **Holographic Memory**: Distributed vector weights across the fleet.
- **MARKOV DECISION PROCESSES**: Implementation of reinforcement learning environments for agentic self-optimization.

---
*Locked under GOLDEN_MASTER_SEAL (v3.7.0-VOYAGER)*
