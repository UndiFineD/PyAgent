# 🤖 PyAgent: The Autonomous Swarm Intelligence (v4.0.0)

PyAgent is a high-performance, multi-agent swarm system optimized for autonomous code improvement, reasoning, and fleet-wide orchestration. It leverages a **Rust-accelerated core** and a **decentralized mixin architecture** to provide a secure, transactionally safe environment for agentic self-evolution.

---

## 🚀 The Core Pillars

### 🐝 Swarm Singularity (v4.0.0)
PyAgent v4.0 has evolved into a fully decentralized "Universal Agent" mesh.
- **Universal Shards**: Agents are no longer specialists; they are shells that load **Logic Manifests** (JSON-defined brains) and **Skills** dynamically.
- **Industrial Factory**: A DAG-based workflow engine that allows agents to execute complex, multi-node logic flows with branching and conditional logic.
- **Synaptic Weights & Topology**: High-fidelity 3D visualization of the swarm with synaptic traffic heatmaps and real-time resource telemetry.
- **Zero-Trust Network**: RSA/HMAC authenticated transport layer with **Signal Double Ratchet** forward secrecy and Byzantine Consensus auditing.

### ⚡ Rust-Native Acceleration
Computationally intensive tasks are delegated to a high-throughput **Rust FFI bridge** (`rust_core`).
- **41% Performance Gain**: Offloads metrics calculation, complexity analysis, and regex FSM decoding to native code.
- **DFA-Based Constraints**: LLM structured output decoding is accelerated via Rust-managed state machines and vectorized bitmasking.
- **Fast Diffs & Patching**: Native Myers diff engine for high-speed code modification and transactional integrity.

### 🐝 Swarm-Mixin Architecture
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

### 🛡️ Transactional FS & Security
PyAgent operates with a **Safety-First** philosophy:
- **State Transactions**: Every file modification is atomic. Automatic rollbacks are triggered if a reasoning chain fails or a collision is detected.
- **Cascading Context**: Prevents infinite recursion and ensures task lineage (Task Parentage -> Result Attribution).
- **Environment Sandbox**: Strict allow-list protocols for external shell operations and PII redaction.
- **End-to-End Encryption**: Signal Protocol implementation for zero-knowledge user data storage. OAuth authentication with cryptographic user isolation ensures server cannot decrypt user memories, chats, or queries.

### 🧠 Advanced LLM Engine (v0.14.0+)
Fully integrated with **vLLM** and custom inference kernels:
- **Speculative Decoding**: Multi-generational token prediction (Medusa/Eagle patterns).
- **Grammar Constraints**: Pydantic-to-Regex-to-FSM conversion for 100% valid JSON/JSONSchema outputs.
- **KV Cache Offloading**: Rust-accelerated RDMA transfer logic for disaggregated prefill/decode.
- **Paged Attention**: Block-based KV management for handling extreme sequence lengths.

---

## 🛠️ Project Ecosystem

| Core Layer | Path | Description |
| :--- | :--- | :--- |
| **Swarm** | `src/logic/agents/` | Specialized agents (Coder, Analyst, **Quantum Scaling Coder**, etc.) |
| **Logic** | `src/logic/` | Shared reasoning cores and metrics engines |
| **Inference** | `src/inference/` | vLLM connectors, streaming, and decoding constraints |
| **Core** | `src/core/base/` | Mixins, state managers, and transactional FS |
| **Skills** | `src/external_candidates/` | Ingested external capabilities and auto-generated tool wrappers |
| **Acceleration**| `rust_core/` | Native PyO3 modules (Performance Kernels) |
| **Observability**| `src/observability/`| Prometheus metrics, stats, and health monitoring |
| **Security**| `src/core/base/logic/security/`| E2EE core, OAuth integration, encrypted memory storage |

---

## 📦 Installation

PyAgent requires **Python 3.12+** and a C++ compiler for the Rust bridge (Maturin).

```powershell
# Clone the fleet
git clone https://github.com/UndiFineD/PyAgent
cd PyAgent

# Initialize Environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install Dependencies (Secure Stack)
pip install -r requirements.txt
```

### 🔧 Building the Rust Core
```powershell
cd rust_core
maturin develop --release
```

---

## 🚦 Quick Start

### Start the Fleet Load Balancer (FastAPI)
```powershell
python -m src.interface.ui.web.py_agent_web --port 8000
```

### Run an Autonomous Task (CLI)
```powershell
python -m src.interface.ui.cli.pyagent_cli --task "Analyze dependencies and optimize imports" --priority HIGHEST
```

### Run Health Audit
```powershell
python -m pytest tests/unit/
```

---

## 🔐 Security & Privacy

PyAgent implements **Signal Protocol** for end-to-end encryption, providing WhatsApp/Signal-level security:

### Zero-Knowledge Architecture
- **OAuth Authentication**: Supports GitHub, Google, and other providers
- **Client-Side Encryption**: User keys never leave the client device
- **Encrypted Storage**: All user memories, chats, and queries encrypted at rest
- **Perfect Forward Secrecy**: Each message uses a unique key via Double Ratchet
- **User Isolation**: Cryptographic guarantee that users cannot access each other's data

### Features
- ✅ **X3DH Key Agreement**: Asynchronous message delivery without online coordination
- ✅ **Double Ratchet Algorithm**: Self-healing encryption with forward secrecy
- ✅ **Multi-Tenant Isolation**: Per-user encryption keys with zero-knowledge server
- ✅ **Encrypted Memory Store**: Transparent E2EE wrapper for existing storage
- ✅ **User-to-User E2EE**: Secure messaging between users and agents

**Documentation**: See [`docs/E2E_ENCRYPTION.md`](docs/E2E_ENCRYPTION.md) for complete usage guide and security properties.

---

## 🗺️ Roadmap "VOYAGER"
- [x] **Decentralized Transport**: Zero-broker P2P swarms with mDNS discovery.
- [x] **Synaptic Pruning**: Exponential knowledge decay for high-efficiency memory.
- [x] **Holographic Memory**: Distributed vector weights across the fleet.
- [x] **Multimodal AI Integration**: Async task queues for image generation and processing, with background artifact cleanup.
- [x] **External Skill Ingestion**: Automated ingestion and wrapping of external Python tools (`external_candidates`).
- [x] **End-to-End Encryption**: Signal Protocol implementation with zero-knowledge user data storage.
- [ ] **MARKOV Decision Processes**: Implementation of RL environments for self-optimization.
- [ ] **Multi-Model Speculation**: Federated speculative decoding across multiple nodes.

---
*Locked under GOLDEN_MASTER_SEAL (v4.0.0-VOYAGER)*

