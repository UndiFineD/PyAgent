# PyAgent Improvement Research & Roadmap

## 🧠 Fleet & Agent Improvements

### 1. High Complexity Modules (Refactoring Target)
- **LLMClient.py (High Complexity)**: Centralized backend logic is growing.
  - *Action*: Planning to shard by provider (vLLM, Ollama, GitHub).
- **SecurityCore.py**: Needs final audit to ensure `LocalContextRecorder` initialization doesn't violate pure core rules.

### 2. Documentation & Traceability
- **Docstring Quality**: Many classes have auto-generated headers with little value.
  - *Action*: FLEET_AUTO_DOC.md is now being generated autonomously by the swarm.

## 🚀 Trillion-Parameter Context Recording Strategy (Phase 108 Optimized)

### 1. Massively Parallel Context Storage
- **Adler-32 Sharding**: Interaction memory is partitioned into 256 shards using stable hashing. This allows the fleet to scale to billions of interactions without JSON lock contention.
- **Monthly Partitions**: interactions_YEAR_MONTH.jsonl.gz provides temporal sharding and high compression (Zlib).

### 2. Relational Intelligence Overlay
- **SQL Metadata (WAL Mode)**: Every shard interaction is indexed in a high-performance SQLite database.
- **Automated Intelligence Harvesting**: The orchestrators autonomously query failure patterns ("lessons") to refine future logic.

## 🛡️ Core/Shell Architecture Design (Phase 114+)

To facilitate the migration of performance-critical logic to Rust, the codebase is being refactored into a **Core/Shell** pattern:

### 1. The Pure Logic Core (`*Core.py`)
- **Responsibility**: Pure computation, data transformation, regex parsing, score calculation.
- **Rules**:
  - No File I/O (cannot use `os`, `sqlite3`, `pathlib.read_text`, etc.).
  - No Network access.
  - No side effects.
  - Strictly typed.
- **Rust Readiness**: These files can be replaced by a compiled module without any changes to surrounding logic.

### 2. The I/O Shell (`Agent.py`, `Manager.py`, `Registry.py`, `Engine.py`)
- **Responsibility**: State management, File I/O, Database calls, Network requests.

## 🚀 Recent Autonomous Findings

### Current Mission: Phase 114 Finalization
- **Target**: 100% type safety and Rust readiness for context engines.
- **Status**: **COMPLETE**.
- **Outcomes**: 
  - `GraphCore.py` and `KnowledgeCore.py` side-effect-free.
  - `ConnectivityManager` singleton consolidation.
  - 836/836 files scanned by self-improvement swarm.

#### 🔍 Top Issues Discovered
- **Redundancy**: Multiple `ConnectivityManager` classes caused fragmented health tracking. Resolved.
- **Side-Effect Seep**: Resolved in `GraphContextEngine` by extracting logic into `GraphCore`.

### 🧠 AI Lessons Derived from Deep Shard Analysis (Phase 108)
- Intelligence Shard 27: Persistent connection pooling reduces latency by 40% in dense agent swarms.
- Intelligence Shard 114: Recursion observed in lazy registries when configs are unreachable. Resolved by attribute guarding.
