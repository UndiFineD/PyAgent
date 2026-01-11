# 📋 Improvements Needed

## 🏗️ Phase 131 Autonomous Scaling (PLANNED)
- [ ] Implement actual PyO3 Rust bindings for `btree_store.py` hashing.
- [ ] Bridge `ShardingOrchestrator` to the `GrafanaGenerator` for real-time cluster visualization.
- [ ] Implement `NeuralPruningEngine` logic in `GraphKnowledgeStore`.
- [ ] Implement production logic for `FutureAgent.py` (Move beyond infrastructure validation stub).
- [ ] Populate `src/logic/agents/specialized/` with personified agents (e.g., Legal, HR, Finance).

## ✅ Completed & Verified (Archive)
- [x] **Graph Sharding**: Implemented in `src/core/knowledge/graph_store.py` using per-node shard files.
- [x] **Autodoc Path Flattening**: `ReportGenerator` now uses underscored relative paths to prevent identifier collisions.
- [x] **Neural Pruning Logic**: `KnowledgePruningEngine` implements time-decayed "Anchoring Strength".
- [x] **GLM-4.7 Cost Benchmarking**: Verified sub-7 cent per million token coding performance in `temp/benchmark_glm47.py`.
- [x] **Hopper Matmul Simulation**: Implemented `HopperSim` FP8 simulation in `temp/simulate_hopper.py`.
- [x] **Concrete Logic Implementation**: Scanned for and verified that all production-ready components are fully implemented.
- [x] **Test Coverage Infrastructure**: Automated gap test generation in `src/infrastructure/dev/agent_tests/agents.py`.
- [x] **Optional Plugin Hooks**: Corrected `AgentPluginBase` to use `pass` for `setup`/`teardown`.
- [x] **Dynamic Communication Sharding**: Implemented `ShardingOrchestrator` to cluster high-frequency agents (Phase 128).
- [x] **Multi-Modal Synchronization**: Integrated synchronization hook in `BTreeKnowledgeStore`.
- [x] **Hopper Optimization**: Integrated `HopperSim` FP8 simulation into `ModelOptimizerAgent`.
- [x] **Latent Reasoning Guardrails**: Implemented `LatentReasoningAgent`.
- [x] **Circular Dependency**: `OrchestratorAgent.py` cross-layer imports moved to abstract providers.
- [x] **Legacy Test Consolidation**: Cleaned up redundant test folders into 5-tier hierarchy.


## 🔍 Codebase Scan Results (Jan 2026)
- **Status**: Root dir and `src/` cleaned. 5-Tier architecture verified with Phase 130 tests.
- **Actionable Tasks Found**:
    - [ ] **Python 3.13 Migration**: Audit agents for `deprecated` modules (e.g., `telnetlib`, `cgi`) before 3.13 final.
    - [ ] **Plugin Sandboxing**: `plugins/` execution needs stricter WASM or Docker isolation to protect the host.
    - [ ] **Rust Core Acceleration**: Implement PyO3 bindings for `btree_store` hashing as planned in Phase 131.

