# Project README
# 🤖 PyAgent: The Autonomous Swarm Intelligence (v4.0.0-VOYAGER)

PyAgent is a high-performance, multi-agent swarm system optimized for autonomous code improvement, reasoning, and fleet-wide orchestration. It leverages a **Rust-accelerated core** and a **decentralized mixin architecture** to provide a secure, transactionally safe environment for agentic self-evolution.

---

## 🚀 The Core Pillars

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
  - **Operational Cost**: Monitors resource utilization and token efficiency.
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
| **Acceleration**| `rust_core/` | Native PyO3 modules (Performance Kernels) |
| **Auto-Fix** | `src/auto_fix/` | Modular rule engine, transaction manager, and CLI for safe automated fixes |

| **Observability**| `src/observability/`| Prometheus metrics, stats, and health monitoring |

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

## 🗺️ Roadmap "VOYAGER"
- [ ] **Decentralized Transport**: Zero-broker P2P swarms with mDNS discovery.
- [ ] **Synaptic Pruning**: Exponential knowledge decay for high-efficiency memory.
- [ ] **Holographic Memory**: Distributed vector weights across the fleet.
- [ ] **Multimodal AI Integration**: Async task queues for image generation and processing, with background artifact cleanup (inspired by 4o-ghibli-at-home).
- [ ] **MARKOV Decision Processes**: Implementation of RL environments for self-optimization.
- [ ] **Multi-Model Speculation**: Federated speculative decoding across multiple nodes.
- [ ] **MARKOV Decision Processes**: Implementation of RL environments for self-optimization.
- [ ] **Multi-Model Speculation**: Federated speculative decoding across multiple nodes.

---
*Locked under GOLDEN_MASTER_SEAL (v4.0.0-VOYAGER)*

## Changelog

### 2026-03-08: FLM (Fastflow Language Model) Integration

**New Feature**: Local NPU-optimized inference provider via OpenAI-compatible API

**What is FLM?** 
FLM (Fastflow Language Model) is a local, OpenAI-compatible model server optimized for NPU-backed inference. PyAgent now supports FLM as a first-class provider alongside cloud and Ollama-like runtimes.

**Key Components Added**:
- **Provider Configuration**: `src/core/providers/FlmProviderConfig.py` - Config validation with required fields (`base_url`, `default_model`, `timeout`, `max_retries`) and optional paths (`health_path`, `chat_path`)
- **Chat Adapter**: `src/core/providers/FlmChatAdapter.py` - OpenAI SDK-compatible adapter supporting:
  - Standard chat completions (`chat.completions.create`)
  - Deterministic tool-call loop with bounded iterations
  - Runtime diagnostics (endpoint availability, model checks)
  - Contextual error handling with actionable messages

**Architecture Design Principles**:
- OpenAI API compatibility first - no custom protocol lock-in
- Local-first reliability - works without cloud dependencies
- NPU-aware performance - optimized for low-overhead local serving
- Deterministic tool-call loop - explicit, testable turn transitions
- Clear operational diagnostics - endpoint/model/timeout logging

**Test Coverage**:
- `tests/test_flm_provider_docs.py` - Documentation verification
- `tests/test_flm_provider_config.py` - Config schema validation (6 tests)
- `tests/test_flm_chat_adapter.py` - Basic adapter functionality (2 tests)
- `tests/test_flm_tool_loop.py` - Tool-call loop and guard triggers (3 tests)
- `tests/test_flm_runtime_errors.py` - Error handling scenarios (2 tests)

**Request/Response Contract**:
1. Client sends completion with `model`, `messages`, `max_tokens`
2. If response contains `tool_calls`: append assistant+tool messages and repeat
3. If no `tool_calls`: return final assistant content
4. Bounded loop guard prevents infinite tool iterations

**Usage Example**:
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:52625/v1/",
    api_key="dummy"  # local placeholder
)

response = client.chat.completions.create(
    model="llama3.2:1b",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=100
)
```

**Security Considerations**:
- FLM is local-network by default
- Compatible with OpenAI client API key handling
- No sensitive content persistence without explicit policy

**Future Enhancements**:
- Dynamic model capability probe (`/models`)
- Streaming response support
- Health-check gate before first inference
- Provider fallback chain (FLM → Ollama → cloud)

**Documentation**:
- Design: `.github/superpower/brainstorm/2026-03-08-flm-design.md`
- Implementation Plan: `.github/superpower/plan/2026-03-08-flm-plan.md`

---

### 2026-03-01: Multimodal Tokenizer

- **Multimodal tokenizer added**: A new `MultimodalTokenizer` provides a unified token space for text, image, audio, and video tokens. It supports pluggable modality-specific tokenizers and a simple fallback implementation. See: `src/infrastructure/engine/tokenization/detokenizer/types.py` and `src/infrastructure/engine/tokenization/detokenizer/simple_tokenizer.py`.

- **Documentation generator fixed for Windows**: `scripts/generate_docs_and_tests.py` now avoids emoji/Unicode characters that fail on Windows consoles (cp1252). The script completed a full run over the repository and generates `.description.md`, `.improvements.md`, `.splice.md`, and `*_test.py` artifacts with a resumable checkpointing mechanism. Use `--dry-run` to preview changes or `--execute` to create files.

- **New tests**: Added lightweight tests and standalone examples for the tokenizer components:
  - `test_tokenizer_protocol.py` — demonstrates Protocol vs implementation
  - `test_multimodal_tokenizer.py` — integration tests for multimodal tokenization
  - `test_multimodal_standalone.py` — quick verification harness

## How to try the new tokenizer

1. Install dev dependencies and activate the virtualenv (see Installation above).
2. Run the standalone verification (no package imports required):

```powershell
python test_multimodal_standalone.py
```

3. Or run the protocol demo and integration tests:

```powershell
python test_tokenizer_protocol.py
python test_multimodal_tokenizer.py
```

If you deploy to CI, ensure `pyproject.toml` or your test runner includes these new tests.

## Tiered context files
- llms-architecture.txt
- llms-improvements.txt

## Notes
Use llms-architecture.txt for architecture and layout rules.
Use llms-improvements.txt for consolidated improvements and lessons.
