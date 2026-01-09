# Rust Conversion Readiness Manifest

This document tracks modules that have been audited, decoupled from side-effects (IO/Network), and are ready for conversion to Rust (via PyO3 or FFI) using the Core/Shell pattern.

## 💎 Primary Core Candidates

| Module | Purpose | Status | Complexity | Typing |
|--------|---------|--------|------------|--------|
| [src/classes/base_agent/core.py](src/classes/base_agent/core.py) | Foundation for all agents (workspace root, path logic, diffs) | READY | Medium | 100% |
| [src/classes/agent/AgentCore.py](src/classes/agent/AgentCore.py) | Logic for improvement parsing, changelog formatting | READY | Medium | 100% |
| [src/classes/fleet/EvolutionCore.py](src/classes/fleet/EvolutionCore.py) | Genetic algorithms for fleet adaptation | READY | Medium | 100% |
| [src/classes/api/APICore.py](src/classes/api/APICore.py) | OpenAPI spec generation and contract validation | READY | Low | 100% |
| [src/classes/orchestration/ToolCore.py](src/classes/orchestration/ToolCore.py) | Argument filtering and metadata extraction logic | READY | Low | 100% |
| [src/classes/stats/FormulaEngineCore.py](src/classes/stats/FormulaEngineCore.py) | AST-based mathematical expression evaluator | READY | High | 100% |
| [src/classes/context/GraphCore.py](src/classes/context/GraphCore.py) | AST-based code relationship analysis | READY | Medium | 100% |
| [src/classes/context/KnowledgeCore.py](src/classes/context/KnowledgeCore.py) | Indexing and search logic for knowledge graph | READY | High | 100% |
| [src/classes/context/GlobalContextCore.py](src/classes/context/GlobalContextCore.py) | Stable sub-sharding and cognitive summary logic | READY | Medium | 100% |
| [src/classes/fleet/AgentRegistryCore.py](src/classes/fleet/AgentRegistryCore.py) | Manifest parsing and version compatibility | READY | Medium | 100% |
| [src/classes/fleet/OrchestratorRegistryCore.py](src/classes/fleet/OrchestratorRegistryCore.py) | Dynamic orchestrator discovery logic | READY | Medium | 100% |
| [src/classes/fleet/FleetCore.py](src/classes/fleet/FleetCore.py) | Tool scoring and state transition logic | READY | Medium | 100% |
| [src/classes/orchestration/SelfHealingCore.py](src/classes/orchestration/SelfHealingCore.py) | Health thresholds and recovery selection | READY | Medium | 100% |
| [src/classes/stats/ModelFallbackCore.py](src/classes/stats/ModelFallbackCore.py) | Fallback chains and cost ranking logic | READY | Low | 100% |
| [src/classes/stats/ObservabilityCore.py](src/classes/stats/ObservabilityCore.py) | Performance aggregation and cost auditing | READY | Medium | 100% |
| [src/classes/orchestration/ConsensusCore.py](src/classes/orchestration/ConsensusCore.py) | Multi-agent voting and tie-breaker logic | READY | Low | 100% |
| [src/classes/orchestration/TaskDecomposerCore.py](src/classes/orchestration/TaskDecomposerCore.py) | Heuristic-based planner and summarizer | READY | Low | 100% |
| [src/classes/fleet/SecretCore.py](src/classes/fleet/SecretCore.py) | Secret masking and validation logic | READY | Low | 100% |
| [src/classes/fleet/TenantCore.py](src/classes/fleet/TenantCore.py) | Path translation and isolation enforcement | READY | Low | 100% |
| [src/classes/fleet/ScalingCore.py](src/classes/fleet/ScalingCore.py) | Load monitoring and scaling decision logic | READY | Low | 100% |
| [src/classes/fleet/EvolutionCore.py](src/classes/fleet/EvolutionCore.py) | Genetic algorithms for fleet adaptation | READY | Medium | 100% |
| [src/classes/fleet/FleetCore.py](src/classes/fleet/FleetCore.py) | Tool scoring and state transition logic | READY | Medium | 100% |
| [src/classes/context/MemoryCore.py](src/classes/context/MemoryCore.py) | Episode scoring and utility decay logic | READY | Low | 100% |
| [src/classes/cognitive/MemoryConsolidatorCore.py](src/classes/cognitive/MemoryConsolidatorCore.py) | Logic for distilling interactions into insights | READY | Medium | 100% |
| [src/classes/cognitive/MetacognitiveCore.py](src/classes/cognitive/MetacognitiveCore.py) | Reasoning certainty and consistency logic | READY | Low | 100% |
| [src/classes/cognitive/TheoryOfMindCore.py](src/classes/cognitive/TheoryOfMindCore.py) | Agent modeling and collaborator ranking logic | READY | Medium | 100% |
| [src/classes/context/ContextCompressorCore.py](src/classes/context/ContextCompressorCore.py) | AST-based signature extraction and summary logic | READY | Medium | 100% |
| [src/classes/coder/SecurityCore.py](src/classes/coder/SecurityCore.py) | Regex scanning & Auditing | READY | Medium | 100% |
| [src/classes/orchestration/SignalCore.py](src/classes/orchestration/SignalCore.py) | Event broadcasting and history windowing | READY | Low | 100% |
| [src/classes/stats/TokenCostCore.py](src/classes/stats/TokenCostCore.py) | Multi-model pricing and usage estimation | READY | Low | 100% |
| [plugins/community_demo/CommunityCore.py](plugins/community_demo/CommunityCore.py) | Example community-contributed logic unit | READY | Low | 100% |
| [plugins/mock_plugin/MockCore.py](plugins/mock_plugin/MockCore.py) | Logic unit for mock plugin demonstrations | READY | Low | 100% |

## 🛠️ Performance-Critical Targets (High Priority)

1.  **FormulaEngine.py**: Complex string parsing and mathematical evaluation.
2.  **KnowledgeCore.py**: High-frequency indexing operations.
3.  **BaseCore.is_path_ignored**: High-frequency path matching during file scans.

## 🧪 Audit Criteria
- [x] **Pure Functions**: No direct calls to os, pathlib.Path.write_text, 
equests, or sqlite3.
- [x] **Explicit State**: Data must be passed in as arguments or held in dataclasses.
- [x] **Strong Typing**: 100% return type hints and parameter annotations.
- [x] **No Multi-processing/Threading**: Logic must be single-threaded (Rust will handle parallelism).

## 🚀 Recent Audits (Phase 114)
- **AgentCore**: Verified side-effect free path calculation.
- **ToolCore**: Audited parameter filtering logic for registry isolation.
- **EvolutionCore**: Verified pure mutation algorithms.
