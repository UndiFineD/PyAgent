# Rust Conversion Readiness Manifest

## 🛠️ RUST IMPLEMENTATION PROMPT LIST (Priority Queue)
- [ ] **[src/infrastructure/orchestration/LockManager.py](src/infrastructure/orchestration/LockManager.py)** (Distributed Locking & Multiprocess Sync)
- [ ] **[src/infrastructure/orchestration/SignalRegistry.py](src/infrastructure/orchestration/SignalRegistry.py)** (Event-driven Concurrency & Capability Discovery)
- [ ] **[src/infrastructure/fleet/AsyncFleetManager.py](src/infrastructure/fleet/AsyncFleetManager.py)** (Sync/Async Workflow Orchestration & Migration)
- [ ] **[src/logic/agents/security/LegalAuditAgent.py](src/logic/agents/security/LegalAuditAgent.py)** (License & Contract Auditing)
- [ ] **[src/core/base/ShardedKnowledgeCore.py](src/core/base/ShardedKnowledgeCore.py)** (High-speed Hashing & Sharding)

## 🛡️ Security Hardening (Phase 240)
- [x] **PyO3 Security Patch**: Upgraded to `0.24.1` to mitigate RUSTSEC-2025-0020 (Buffer overflow in `PyString::from_object`).
- [x] **Bound API Migration**: Ported `rust_core` to the modern `Bound` API for thread-safe memory management.

This document tracks modules that have been audited, decoupled from side-effects (IO/Network), and are ready for conversion to Rust (via PyO3 or FFI) using the Core/Shell pattern.

## 💎 Primary Core Candidates

| Module | Purpose | Status | Complexity | Typing |
|--------|---------|--------|------------|--------|
| [src/infrastructure/fleet/AsyncFleetManager.py](src/infrastructure/fleet/AsyncFleetManager.py) | **Zero-Downtime Agent Migration & Parallel Workflow execution (Phase 239)** | READY | High | 100% |
| [src/logic/agents/security/LegalAuditAgent.py](src/logic/agents/security/LegalAuditAgent.py) | **License Blacklist enforcement & Smart Contract auditing (Phase 238)** | READY | Medium | 100% |
| [src/core/base/ShardedKnowledgeCore.py](src/core/base/ShardedKnowledgeCore.py) | **Adler-32 sharding & Right to be Forgotten pruning (Phase 238)** | READY | High | 100% |
| [src/infrastructure/orchestration/DreamStateOrchestrator.py](src/infrastructure/orchestration/DreamStateOrchestrator.py) | **Recursive Skill Synthesis & Simulated Task Practice (Phase 237)** | READY | High | 100% |
| [src/infrastructure/orchestration/GossipProtocolOrchestrator.py](src/infrastructure/orchestration/GossipProtocolOrchestrator.py) | **Epidemic Synchronization & Decentralized State Consistency (Phase 237)** | READY | Medium | 100% |
| [src/core/base/ArchitectureMapper.py](src/core/base/ArchitectureMapper.py) | **Mermaid C4 System Context Generator (Phase 236)** | READY | Medium | 100% |
| [src/core/base/IncrementalProcessor.py](src/core/base/IncrementalProcessor.py) | **BLAKE3 hashing & mmap-backed state serialization (Phase 233)** | READY | High | 100% |
| [src/infrastructure/fleet/ShardingOrchestrator.py](src/infrastructure/fleet/ShardingOrchestrator.py) | **DBSCAN-based agent clustering & live migration logic (Phase 234)** | READY | High | 100% |
| [version.py](version.py) | **Evolution Phase 235: Proxima Edition Gold Master** | READY | Low | 100% |
| [src/interface/ui/cli/pyagent_cli.py](src/interface/ui/cli/pyagent_cli.py) | **Rich CLI with state-aware spinners & topology maps (Phase 235)** | READY | Medium | 100% |
| [src/core/base/DependencyGraph.py](src/core/base/DependencyGraph.py) | **Topological batching & cycle detection (Phase 232)** | READY | Medium | 100% |
| [src/observability/core/LoggingCore.py](src/observability/core/LoggingCore.py) | **High-throughput log masking & RFC3339 formatting (Phase 227)** | READY | Low | 100% |
| [src/infrastructure/fleet/core/GPUMonitorCore.py](src/infrastructure/fleet/core/GPUMonitorCore.py) | **GPU Telemetry, Memory Tracking, and VRAM pressure logic (Phase 227)** | READY | Medium | 100% |
| [src/core/base/managers/PluginManager.py](src/core/base/managers/PluginManager.py) | **Plugin discovery, manifest enforcement, and health check logic (Phase 226)** | READY | Medium | 100% |
| [src/observability/stats/observability_core.py](src/observability/stats/observability_core.py) | **Consolidated observability logic & telemetry aggregation (Phase 224)** | READY | Medium | 100% |
| [src/core/base/](src/core/base/) | **Global Type Conformance & Future Annotations (Phase 221)** | READY | Low | 100% |
| [src/logic/agents/cognitive/core/MemoryConsolidatorCore.py](src/logic/agents/cognitive/core/MemoryConsolidatorCore.py) | **Logic for distilling interactions into insights (Phase 219)** | READY | Medium | 100% |
| [src/core/base/managers/ProcessorManagers.py](src/core/base/managers/ProcessorManagers.py) | **Binary serialization (CBOR/Pickle) & compression logic (Phase 218)** | READY | Medium | 100% |
| [src/infrastructure/dev/scripts/FleetHarness.py](src/infrastructure/dev/scripts/FleetHarness.py) | **Unified command management for fleet operations (Phase 217)** | READY | Low | 100% |
| [src/core/knowledge/btree_store.py](src/core/knowledge/btree_store.py) | **Concurrent B-Link Tree & Mmap caching (Phase 216)** | READY | High | 100% |
| [src/core/knowledge/storage_base.py](src/core/knowledge/storage_base.py) | **Abstract storage interface for knowledge sharding (Phase 216)** | READY | Low | 100% |
| [src/logic/cognitive/prompt_templates.py](src/logic/cognitive/prompt_templates.py) | **Vibe-Coding 2025 track logic & persona mapping (Phase 215)** | READY | Low | 100% |
| [src/core/base/core/PruningCore.py](src/core/base/core/PruningCore.py) | **Decay & Synaptic weight logic (Phase 214)** | READY | High | 100% |
| [src/logic/agents/development/core/BenchmarkCore.py](src/logic/agents/development/core/BenchmarkCore.py) | **Latency regression gate logic (Phase 213)** | READY | Low | 100% |
| [src/observability/stats/core/TracingCore.py](src/observability/stats/core/TracingCore.py) | **OTel span logic & Thinking/Network latency (Phase 201)** | READY | Low | 100% |
| [src/infrastructure/sandbox/core/SandboxCore.py](src/infrastructure/sandbox/core/SandboxCore.py) | **Container isolation & resource limits (Phase 202)** | READY | Low | 100% |
| [src/logic/agents/compliance/core/ComplianceCore.py](src/logic/agents/compliance/core/ComplianceCore.py) | **Continuous compliance & regulatory scanning (Phase 203)** | READY | Low | 100% |
| [src/logic/agents/development/core/ToolDraftingCore.py](src/logic/agents/development/core/ToolDraftingCore.py) | **Dynamic OpenAPI tool generation (Phase 204)** | READY | Medium | 100% |
| [src/infrastructure/fleet/core/LoadBalancerCore.py](src/infrastructure/fleet/core/LoadBalancerCore.py) | **Cognitive load balancing & pressure scaling (Phase 205)** | READY | Low | 100% |
| [src/logic/agents/swarm/core/LessonCore.py](src/logic/agents/swarm/core/LessonCore.py) | **Cross-fleet lesson bloom filters (Phase 206)** | READY | Medium | 100% |
| [src/core/base/core/IdentityCore.py](src/core/base/core/IdentityCore.py) | **Decentralized Agent ID & signing (Phase 207)** | READY | Low | 100% |
| [src/core/base/core/AuthCore.py](src/core/base/core/AuthCore.py) | **Zero-knowledge agent authentication (Phase 208)** | READY | Medium | 100% |
| [src/logic/agents/cognitive/core/LocalRAGCore.py](src/logic/agents/cognitive/core/LocalRAGCore.py) | **Localized vector sharding (Phase 209)** | READY | High | 100% |
| [src/observability/stats/core/StabilityCore.py](src/observability/stats/core/StabilityCore.py) | **Fleet stability & coherence heuristics (Phase 210)** | READY | Medium | 100% |
| [src/logic/agents/security/core/RedQueenCore.py](src/logic/agents/security/core/RedQueenCore.py) | **Adversarial prompt evolution (Phase 211)** | READY | High | 100% |
| [src/observability/stats/core/ProfilingCore.py](src/observability/stats/core/ProfilingCore.py) | **cProfile aggregation & bottleneck logic (Phase 212)** | READY | Low | 100% |
| [src/core/base/core/AutonomyCore.py](src/core/base/core/AutonomyCore.py) | **Agent self-model and autonomy daemon (Phase 200)** | READY | Low | 100% |
| [src/interface/core/InterfaceSyncCore.py](src/interface/core/InterfaceSyncCore.py) | **Unified interface theme and sync (Phase 199)** | READY | Low | 100% |
| [src/logic/agents/system/core/ConfigHygieneCore.py](src/logic/agents/system/core/ConfigHygieneCore.py) | **JSON Schema validation and env mapping (Phase 174)** | READY | Low | 100% |
| [src/logic/agents/documentation/core/TopologyCore.py](src/logic/agents/documentation/core/TopologyCore.py) | **Mermaid.js graph generation logic (Phase 169)** | READY | Low | 100% |
| [src/logic/agents/security/core/ByzantineCore.py](src/logic/agents/security/core/ByzantineCore.py) | **Consensus voting and agreement logic (Phase 168)** | READY | Low | 100% |
| [src/logic/agents/cognitive/core/VisionCore.py](src/logic/agents/cognitive/core/VisionCore.py) | **Visual processing and glitch detection (Phase 167)** | READY | Medium | 100% |
| [src/infrastructure/orchestration/HolographicStateOrchestrator.py](src/infrastructure/orchestration/HolographicStateOrchestrator.py) | **State sharding and reconstruction via bit-packing (Phase 162)** | READY | High | 100% |
| [src/infrastructure/orchestration/TaskDecomposerCore.py](src/infrastructure/orchestration/TaskDecomposerCore.py) | **Heuristic planning and dependency analysis** | READY | Medium | 100% |
| [src/infrastructure/fleet/AgentEconomy.py](src/infrastructure/fleet/AgentEconomy.py) | **Market Pricing & Agent Accounting Engine** | READY | Low | 100% |
| [src/core/base/acceleration.py](src/core/base/acceleration.py) | **Calculate Synaptic Weight (NeuralPruningEngine)** | READY | High | 100% |
| [src/core/base/BaseAgent.py](src/core/base/BaseAgent.py) | Foundation for all agents (workspace root, path logic, diffs) | READY | Medium | 100% |
| [src/infrastructure/fleet/EvolutionCore.py](src/infrastructure/fleet/EvolutionCore.py) | Genetic algorithms for fleet adaptation | READY | Medium | 100% |
| [src/infrastructure/api/APICore.py](src/infrastructure/api/APICore.py) | OpenAPI spec generation and contract validation | READY | Low | 100% |
| [src/infrastructure/orchestration/ToolCore.py](src/infrastructure/orchestration/ToolCore.py) | Argument filtering and metadata extraction logic | READY | Low | 100% |
| [src/observability/stats/FormulaEngineCore.py](src/observability/stats/FormulaEngineCore.py) | AST-based mathematical expression evaluator | READY | High | 100% |
| [src/logic/agents/cognitive/context/engines/GraphCore.py](src/logic/agents/cognitive/context/engines/GraphCore.py) | AST-based code relationship analysis | READY | Medium | 100% |
| [src/logic/agents/cognitive/context/engines/KnowledgeCore.py](src/logic/agents/cognitive/context/engines/KnowledgeCore.py) | Indexing and search logic for knowledge graph | READY | High | 100% |
| [src/logic/agents/cognitive/context/engines/GlobalContextCore.py](src/logic/agents/cognitive/context/engines/GlobalContextCore.py) | Stable sub-sharding and conflict resolution logic | READY | Medium | 100% |
| [src/infrastructure/fleet/AgentRegistryCore.py](src/infrastructure/fleet/AgentRegistryCore.py) | Manifest parsing and circular dependency detection | READY | Medium | 100% |
| [src/infrastructure/fleet/ScalingCore.py](src/infrastructure/fleet/ScalingCore.py) | Proactive multi-resource scaling and anti-flapping | READY | Medium | 100% |
| [src/logic/agents/cognitive/context/engines/MemoryCore.py](src/logic/agents/cognitive/context/engines/MemoryCore.py) | Episode scoring and utility decay logic | READY | Low | 100% |
| [src/logic/agents/cognitive/core/MetacognitiveCore.py](src/logic/agents/cognitive/core/MetacognitiveCore.py) | Reasoning certainty and consistency logic | READY | Low | 100% |
| [src/logic/agents/cognitive/core/TheoryOfMindCore.py](src/logic/agents/cognitive/core/TheoryOfMindCore.py) | Agent modeling and collaborator ranking logic | READY | Medium | 100% |
| [src/logic/agents/cognitive/context/engines/ContextCompressorCore.py](src/logic/agents/cognitive/context/engines/ContextCompressorCore.py) | AST-based signature extraction and summary logic | READY | Medium | 100% |
| [src/logic/agents/development/SecurityCore.py](src/logic/agents/development/SecurityCore.py) | Regex scanning & Auditing | READY | Medium | 100% |
| [src/infrastructure/orchestration/SignalCore.py](src/infrastructure/orchestration/SignalCore.py) | Event broadcasting and history windowing | READY | Low | 100% |
| [src/observability/stats/TokenCostCore.py](src/observability/stats/TokenCostCore.py) | Multi-model pricing and usage estimation | READY | Low | 100% |
| [src/logic/agents/intelligence/SearchCore.py](src/logic/agents/intelligence/SearchCore.py) | Pure logic for search result parsing and Markdown formatting | READY | Medium | 100% |
| [src/logic/agents/intelligence/WebCore.py](src/logic/agents/intelligence/WebCore.py) | Pure logic for HTML cleaning and link extraction | READY | Low | 100% |
| [src/logic/agents/development/DependencyCore.py](src/logic/agents/development/DependencyCore.py) | AST-based dependency and inheritance analysis | READY | Medium | 100% |
| [src/logic/agents/development/ArchCore.py](src/logic/agents/development/ArchCore.py) | Architectural metrics and coupling calculations | READY | Low | 100% |
| [src/infrastructure/orchestration/ConsensusCore.py](src/infrastructure/orchestration/ConsensusCore.py) | Weighted voting and agreement score calculation | READY | Low | 100% |
| [src/infrastructure/orchestration/SelfHealingCore.py](src/infrastructure/orchestration/SelfHealingCore.py) | Anomaly detection and recovery state logic | READY | Medium | 100% |
| [src/infrastructure/fleet/KnowledgeTransferCore.py](src/infrastructure/fleet/KnowledgeTransferCore.py) | Lesson dataset merging and deduplication logic | READY | Low | 100% |
| [src/logic/agents/development/DocGenCore.py](src/logic/agents/development/DocGenCore.py) | AST-based documentation extraction and formatting | READY | Medium | 100% |
| [src/logic/agents/intelligence/ResearchCore.py](src/logic/agents/intelligence/ResearchCore.py) | SGI-Bench DCAP cycle logic and tool drafting | READY | Medium | 100% |
| [src/logic/agents/development/CodeQualityCore.py](src/logic/agents/development/CodeQualityCore.py) | Pure logic for cross-language quality checks | READY | Low | 100% |
| [src/logic/agents/development/TechDebtCore.py](src/logic/agents/development/TechDebtCore.py) | AST-based technical debt analysis and hotspotting | READY | Medium | 100% |


## 🔥 Performance-Critical Targets (High Priority)

1.  **[src/infrastructure/fleet/AsyncFleetManager.py](src/infrastructure/fleet/AsyncFleetManager.py)**: Async migration and workflow orchestration. Critical for zero-downtime swarm intelligence.
2.  **[src/core/base/core/PruningCore.py](src/core/base/core/PruningCore.py)**: Bio-digital synaptic decay logic. Essential for swarm stability and performance under high cognitive pressure.
3.  **[src/logic/agents/security/core/RedQueenCore.py](src/logic/agents/security/core/RedQueenCore.py)**: Adversarial mutation logic. Core security loop for evolving against prompt injection.
4.  **[src/core/knowledge/btree_store.py](src/core/knowledge/btree_store.py)**: Sharded B-Tree logic. MD5 path calculation and page sharding math.
5.  **[src/core/knowledge/graph_store.py](src/core/knowledge/graph_store.py)**: Sharded ontological graph. Node-level MD5 sharding and triple store lookups.
6.  **[src/infrastructure/fleet/ShardingOrchestrator.py](src/infrastructure/fleet/ShardingOrchestrator.py)**: Dynamic clustering algorithms for trillion-parameter data isolation.
7.  **[src/logic/agents/intelligence/LatentReasoningAgent.py](src/logic/agents/intelligence/LatentReasoningAgent.py)**: Chain-of-thought verification logic and linguistics auditing.
8.  **[src/logic/agents/system/ModelOptimizerAgent.py](src/logic/agents/system/ModelOptimizerAgent.py)**: Quantization (FP8/Hopper) logic and cost/latency trade-off simulations.

## 🧪 Audit Criteria
- [x] **Pure Functions**: No direct calls to os (except path math), requests, or db.
- [x] **Explicit State**: Data must be passed in as arguments or held in dataclasses.
- [x] **Strong Typing**: 100% return type hints and parameter annotations.
- [x] **PyO3 Compatibility**: Struct-based layout ready for Rust transition.

## 🚀 Recent Audits (Phase 130)
- **BTreeKnowledgeStore**: Verified MD5 sharding purity for high-scale isolation.
- **LatentReasoningAgent**: Audited the reasoning audit hook for side-effect isolation.
- **ModelOptimizerAgent**: Validated Hopper simulation logic for 100% typing.

## 🚀 Recent Audits (Phase 114)
- **BaseAgent**: Verified side-effect free path calculation.
- **ToolCore**: Audited parameter filtering logic for registry isolation.
- **EvolutionCore**: Verified pure mutation algorithms."
