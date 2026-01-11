# Rust Conversion Readiness Manifest

This document tracks modules that have been audited, decoupled from side-effects (IO/Network), and are ready for conversion to Rust (via PyO3 or FFI) using the Core/Shell pattern.

## 💎 Primary Core Candidates

| Module | Purpose | Status | Complexity | Typing |
|--------|---------|--------|------------|--------|
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
| [src/logic/agents/cognitive/core/MemoryConsolidatorCore.py](src/logic/agents/cognitive/core/MemoryConsolidatorCore.py) | Logic for distilling interactions into insights | READY | Medium | 100% |
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
| [src/infrastructure/orchestration/TaskDecomposerCore.py](src/infrastructure/orchestration/TaskDecomposerCore.py) | Heuristic planning and dependency analysis | READY | Medium | 100% |
| [src/infrastructure/orchestration/ConsensusCore.py](src/infrastructure/orchestration/ConsensusCore.py) | Weighted voting and agreement score calculation | READY | Low | 100% |
| [src/infrastructure/orchestration/SelfHealingCore.py](src/infrastructure/orchestration/SelfHealingCore.py) | Anomaly detection and recovery state logic | READY | Medium | 100% |
| [src/infrastructure/fleet/KnowledgeTransferCore.py](src/infrastructure/fleet/KnowledgeTransferCore.py) | Lesson dataset merging and deduplication logic | READY | Low | 100% |
| [src/logic/agents/development/DocGenCore.py](src/logic/agents/development/DocGenCore.py) | AST-based documentation extraction and formatting | READY | Medium | 100% |
| [src/logic/agents/intelligence/ResearchCore.py](src/logic/agents/intelligence/ResearchCore.py) | SGI-Bench DCAP cycle logic and tool drafting | READY | Medium | 100% |
| [src/logic/agents/development/CodeQualityCore.py](src/logic/agents/development/CodeQualityCore.py) | Pure logic for cross-language quality checks | READY | Low | 100% |
| [src/logic/agents/development/TechDebtCore.py](src/logic/agents/development/TechDebtCore.py) | AST-based technical debt analysis and hotspotting | READY | Medium | 100% |


## 🔥 Performance-Critical Targets (High Priority)

1.  **[src/core/knowledge/btree_store.py](src/core/knowledge/btree_store.py)**: Sharded B-Tree logic. MD5 path calculation and page sharding math.
2.  **[src/core/knowledge/graph_store.py](src/core/knowledge/graph_store.py)**: Sharded ontological graph. Node-level MD5 sharding and triple store lookups.
3.  **[src/infrastructure/fleet/ShardingOrchestrator.py](src/infrastructure/fleet/ShardingOrchestrator.py)**: Dynamic clustering algorithms for trillion-parameter data isolation.
3.  **[src/logic/agents/intelligence/LatentReasoningAgent.py](src/logic/agents/intelligence/LatentReasoningAgent.py)**: Chain-of-thought verification logic and linguistics auditing.
4.  **[src/logic/agents/system/ModelOptimizerAgent.py](src/logic/agents/system/ModelOptimizerAgent.py)**: Quantization (FP8/Hopper) logic and cost/latency trade-off simulations.

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
- **EvolutionCore**: Verified pure mutation algorithms.
