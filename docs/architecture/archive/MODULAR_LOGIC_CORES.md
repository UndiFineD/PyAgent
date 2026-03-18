# Modular Logic Cores (`*Core`)

PyAgent follows a **Domain Logic Separation** pattern. Instead of bloating Agent classes with algorithmic complexity, heavy processing is delegated to specialized `*Core` classes located primarily in `src/core/base/logic/core/`.

## The Core Philosophy
1.  **Pure Computation**: Cores should be as deterministic as possible, focusing on data transformation and algorithmic decisions.
2.  **No Prompting**: Cores do not call LLMs. They receive the results of LLM calls or providing grounding data for them.
3.  **Rust Acceleration**: High-performance cores are often backed by `rust_core` for sub-millisecond execution.

## Key Cores & Responsibilities

### 🧬 Evolution & Learning
- **`EvolutionCore.py`**: Tracks agent performance (success rate, usage count) and handles tier-based promotion (Specialized -> Integrated -> Elite).
- **`LessonCore.py`**: Aggregates "Failures" and "Reflections" into a shared lesson database.
- **`SkillManagerCore.py`**: Manages the versioning and lifecycle of ad-hoc scripts into reusable agent skills.

### 🛡️ Safety & Governance
- **`GuardrailCore.py`**: Performs post-generation Pydantic validation and content moderation.
- **`AuthCore.py`**: Manages RBAC (Role-Based Access Control) for tool execution.
- **`ResilienceCore.py`**: Implements circuit breakers and retry logic for brittle infra dependencies.

### 🧠 Memory & Context
- **`MemoryConsolidationCore.py`**: Implements exponential decay, semantic clustering, and LSH-based retrieval for long-term memory.
- **`CodeAnalyzer.py`**: Uses AST surgery to compress source code into compact API summaries for context-injection.
- **`ContextPruningCore.py`**: Dynamic pruning of KV shards based on attention-entropy maps.

### 🏗️ Task Orchestration & Workflows
- **`UniversalAgent.py`**: The cognitive entry point (Pillar 3). Routes intents to specialized cores.
- **`WorkflowExecutor.py`**: executes branching DAGs defined in Logic Manifests (Pillar 4).
- **`FleetConsensusManager.py`**: Handles BFT Raft consensus for high-stakes swarm decisions (Pillar 1).

### 🧠 Memory & Context Scaling (Pillar 2)
- **`KVCacheManager.py`**: Paged Attention KV-cache management with Rust-accelerated block handling.
- **`MemoryConsolidationCore.py`**: Synaptic decay and cluster-based retrieval.

### 📡 Multimodal Processing
- **`AudioStreamCore.py`**: Real-time RTP audio normalization (u-law to PCM) and resampling.
- **`VideoAnalyzerCore.py`**: Temporal sliding window fragmentation for long-form video analysis.
- **`BrowserOutlineCore.py`**: Transforms raw DOM data into high-density "Outlines" for efficient agent navigation.

### 📉 Metrics & Performance
- **`MetricsEngine.py`**: Aggregates throughput, latency, and success metrics across the swarm.
- **`ConvergenceCore.py`**: Detects when an agent's reasoning has reached a stable "Grokking" state.

---
*Cohesion > Integration. Cores enable a self-improving fleet.*
