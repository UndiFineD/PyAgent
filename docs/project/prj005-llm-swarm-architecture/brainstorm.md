# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# LLM Swarm Architecture Design

## Overview
PyAgent is a high-performance, multi-agent swarm system optimized for autonomous code improvement, reasoning, and fleet-wide orchestration. It leverages a **Rust-accelerated core** and a **decentralized mixin architecture** to provide a secure, transactionally safe environment for agentic self-evolution.

## Core Architecture Pillars

### 1. Swarm-Mixin Architecture
PyAgent avoids monolithic design by utilizing a **Synaptic Modularization** pattern. Agents are composed of specialized mixins and categorized into functional swarms:

- **Specialized Agents**:
  - **Quantum Scaling Coder**: Optimizes code for extreme performance and scalability.
  - **Legal Audit**: Ensures compliance and legal safety in autonomous operations.
  - **Operational Cost**: Monitored resource utilization and token efficiency.
- **Mixins**:
  - **ReflectionMixin**: Enables autonomous self-critique and logic verification.
  - **KnowledgeMixin**: Accesses the "Knowledge Trinity" (Structured, Semantic, and Relational memory).
  - **IdentityMixin**: Decouples agent identity from implementation, enabling anonymous peer-to-peer transport.
  - **PersistenceMixin**: Manages atomic state serialization and binary shard snapshots (msgpack/blake3).

### 2. Rust-Native Acceleration
Computationally intensive tasks are delegated to a high-throughput **Rust FFI bridge** (`rust_core`).
- **41% Performance Gain**: Offloads metrics calculation, complexity analysis, and regex FSM decoding to native code.
- **DFA-Based Constraints**: LLM structured output decoding is accelerated via Rust-managed state machines and vectorized bitmasking.
- **Fast Diffs & Patching**: Native Myers diff engine for high-speed code modification and transactional integrity.

### 3. Transactional File System & Security
PyAgent operates with a **Safety-First** philosophy:
- **State Transactions**: Every file modification is atomic. Automatic rollbacks are triggered if a reasoning chain fails or a collision is detected.
- **Cascading Context**: Prevents infinite recursion and ensures task lineage (Task Parentage -> Result Attribution).
- **Environment Sandbox**: Strict allow-list protocols for external shell operations and PII redaction.

### 4. Advanced LLM Engine (v0.14.0+)
Fully integrated with **vLLM** and custom inference kernels:
- **Speculative Decoding**: Multi-generational token prediction (Medusa/Eagle patterns).
- **Grammar Constraints**: Pydantic-to-Regex-to-FSM conversion for 100% valid JSON/JSONSchema outputs.
- **KV Cache Offloading**: Rust-accelerated RDMA transfer logic for disaggregated prefill/decode.
- **Paged Attention**: Block-based KV management for handling extreme sequence lengths.

## Project Ecosystem Structure

| Core Layer | Path | Description |
| :--- | :--- | :--- |
| **Swarm** | `src/logic/agents/` | Specialized agents (Coder, Analyst, **Quantum Scaling Coder**, etc.) |
| **Logic** | `src/logic/` | Shared reasoning cores and metrics engines |
| **Inference** | `src/inference/` | vLLM connectors, streaming, and decoding constraints |
| **Core** | `src/core/base/` | Mixins, state managers, and transactional FS |
| **Acceleration**| `rust_core/` | Native PyO3 modules (Performance Kernels) |
| **Auto-Fix** | `src/auto_fix/` | Modular rule engine, transaction manager, and CLI for safe automated fixes |
| **Observability**| `src/observability/`| Prometheus metrics, stats, and health monitoring |

## Communication & Coordination Patterns

### P2P CRDT Architecture
- **Peer-to-Peer Networking**: Built on Rust libp2p for decentralized communication between agents.
- **Conflict-Free Replicated Data Types (CRDT)**: Ensures eventual consistency across the swarm without central coordination.
- **Automerge Integration**: Leverages Automerge-rs for automatic conflict resolution in shared state.

### Agent Communication
- **Anonymous Peer-to-Peer Transport**: IdentityMixin enables anonymous communication between agents.
- **Task Parentage**: Maintains lineage of tasks and their results for accountability and debugging.
- **Result Attribution**: Ensures proper attribution of results to originating agents.

## Security Architecture

### Data Protection
- **Inline Encryption**: All user data, agent states, and shared memory blocks are encrypted and decrypted in real-time by the Rust layer.
- **Key Lifecycle Management**: Monthly key rotation managed autonomously by the Rust core.
- **Data Sanitization**: Context is scrubbed before any remote API calls to prevent data leakage.

### Access Control
- **Environment Sandbox**: Strict allow-list protocols for external shell operations.
- **PII Redaction**: Automatic redaction of personally identifiable information.
- **Transactional Integrity**: Atomic operations with automatic rollback on failure.

## Implementation Strategy

### Layered Architecture
1. **Core Layer**: Base mixins, state management, and transactional systems
2. **Logic Layer**: Shared reasoning engines and metrics
3. **Agent Layer**: Specialized agents with specific capabilities
4. **Interface Layer**: CLI and web interfaces
5. **Tool Layer**: External tools and utilities
6. **Plugin Layer**: Extensible plugin system with validation

### Technology Stack
- **Python 3.12+**: Primary application logic
- **Rust**: Performance-critical components and security functions
- **vLLM**: High-performance LLM inference
- **Automerge-rs**: CRDT implementation for distributed state
- **libp2p**: Peer-to-peer networking
- **FastAPI**: Web interface and API layer

## Deployment & Scalability

### Fleet Load Balancer
- **Central Coordination**: Manages task distribution across the agent swarm
- **Load Balancing**: Distributes computational load efficiently
- **Health Monitoring**: Tracks agent health and performance metrics

### Resource Management
- **Operational Cost Monitoring**: Tracks resource utilization and token efficiency
- **Quantum Scaling**: Optimizes code for extreme performance and scalability
- **Memory Management**: Efficient handling of shared memory blocks
