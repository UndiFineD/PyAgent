# PyAgent: 317-Phase Swarm Architecture (SYNAPTIC ACCELERATION)

## Overview
PyAgent has evolved from a single-agent orchestrator into a multi-agent swarm capable of autonomous, secure, and transactionally safe self-improvement. Following the **Phase 317 (Synaptic Acceleration)** milestone, the system now features a hybrid Python/Rust core for high-performance indexing and complexity analysis.

## Core Architectural Pillars

### 1. Rust Bridge & Acceleration (`rust_core/`)
The primary performance layer is now a Rust-based FFI bridge (`rust_core.pyd`).
- **37% Acceleration**: CPU-bound tasks like cyclomatic complexity calculation, pattern matching, and JSON logging are delegated to Rust.
- **Complexity Guard**: Sub-millisecond analysis of workspace complexity, enabling the "Phase 317 Complexity Sink" which targets files with complexity > 25.

### 2. Cascade Context and Lineage (`src/core/base/`)
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

## Future Roadmap: Project "VOYAGER"
- **P2P Swarms**: Decentralized fleet synchronization without a central manager.
- **Cross-Language Rust Port**: Low-level migration of core logic to `rust_core/`.
- **Holographic Memory**: Distributed vector weights across the fleet.

---
*Locked under GOLDEN_MASTER_SEAL (v2.2.0-ALFA)*
