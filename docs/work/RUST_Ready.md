# Rust Conversion Readiness - PyAgent Core Modules

This document tracks Python files that are ready or nearly ready for Rust conversion. These files typically contain pure logic, minimal I/O, clear interfaces, and high computational value.

## Status Legend
- ✅ **READY** - Pure logic, no I/O, well-typed, good candidate
- 🔄 **NEAR-READY** - Minimal I/O or dependencies, needs minor cleanup
- ⚠️ **NEEDS-WORK** - Has I/O or complex dependencies, requires refactoring first
- 📊 **HIGH-VALUE** - Performance-critical, would benefit most from Rust

---

## TIER 1: READY FOR IMMEDIATE CONVERSION (18 files)

### Core Base Logic (src/core/base/core/)
1. ✅📊 **ErrorMappingCore.py** - Pure error code mapping
   - Size: ~71 lines
   - Dependencies: None (just dict mappings)
   - Rust benefit: Type safety for error codes
   - Priority: HIGH (used across entire system)

2. ✅📊 **AutonomyCore.py** - Self-model and daemon sleep calculation
   - Size: ~50 lines
   - Dependencies: Basic types only
   - Rust benefit: Performance for optimization scoring
   - Priority: MEDIUM

3. ✅ **ConvergenceCore.py** - Convergence detection logic
   - Size: Small
   - Dependencies: Minimal
   - Rust benefit: Fast convergence calculations

4. ✅ **IdentityCore.py** - Agent identity and hashing
   - Size: Small
   - Dependencies: Minimal
   - Rust benefit: Fast hash operations

5. ✅ **PruningCore.py** - Agent pruning logic
   - Size: Small
   - Dependencies: Minimal
   - Rust benefit: Performance for large fleets

6. ✅ **ResilienceCore.py** - Resilience scoring
   - Size: Small
   - Dependencies: Minimal
   - Rust benefit: Fast resilience calculations

7. ✅ **AuthCore.py** - Authentication logic
   - Size: Small
   - Dependencies: Minimal (may need crypto library)
   - Rust benefit: Security + performance

### Performance & Benchmarking (src/logic/agents/development/core/)
8. ✅📊 **BenchmarkCore.py** - Benchmark calculations
   - Size: ~50 lines
   - Dependencies: dataclass only
   - Rust benefit: HIGH - performance benchmarking should be fast
   - Priority: HIGH

### Statistics & Analysis (src/observability/stats/)
9. ✅📊 **FormulaEngineCore.py** - AST-based formula evaluation
   - Size: ~150 lines
   - Dependencies: ast, operator, math
   - Rust benefit: VERY HIGH - computational core
   - Priority: CRITICAL

10. ✅📊 **TokenCostCore.py** - Token cost calculations
    - Size: ~50 lines
    - Dependencies: Basic math
    - Rust benefit: HIGH - called frequently
    - Priority: HIGH

11. ✅📊 **ModelFallbackCore.py** - Model fallback logic
    - Size: ~100 lines
    - Dependencies: Basic types
    - Rust benefit: Performance for model selection
    - Priority: MEDIUM

12. ✅📊 **ProfilingCore.py** - Profile analysis
    - Size: ~80 lines
    - Dependencies: Stats structures
    - Rust benefit: HIGH - profiling should be fast
    - Priority: HIGH

13. ✅📊 **StabilityCore.py** - Stability scoring
    - Size: ~100 lines
    - Dependencies: Basic math
    - Rust benefit: Performance for stability checks
    - Priority: HIGH

14. ✅📊 **TracingCore.py** - Distributed tracing logic
    - Size: ~60 lines
    - Dependencies: Basic types, time
    - Rust benefit: LOW latency tracing
    - Priority: HIGH

### Agent Core Logic (src/logic/agents/)
15. ✅ **AuctionCore.py** - Auction bid calculations
    - Size: Small
    - Dependencies: Minimal
    - Rust benefit: Fast auction resolution

16. ✅ **ByzantineCore.py** - Byzantine consensus
    - Size: Small
    - Dependencies: Minimal
    - Rust benefit: Performance + security

17. ✅ **PrivacyCore.py** - Privacy calculations
    - Size: Small
    - Dependencies: Minimal
    - Rust benefit: Security + performance

18. ✅ **DeduplicationCore.py** - Deduplication logic
    - Size: Small (~50 lines)
    - Dependencies: Basic types
    - Rust benefit: Performance for large datasets

---

## TIER 2: NEAR-READY (Needs Minor Cleanup) (25 files)

### Context & Memory Engines (src/logic/agents/cognitive/context/engines/)
19. 🔄 **MemoryCore.py** - Memory utility calculations
    - Issue: May have some I/O for persistence
    - Fix: Extract pure logic to MemoryLogicCore

20. 🔄 **KnowledgeCore.py** - Knowledge graph operations
    - Issue: Graph persistence
    - Fix: Separate computation from storage

21. 🔄 **GraphCore.py** - Graph algorithms
    - Issue: File I/O for graph storage
    - Fix: Extract pure graph algorithms

22. 🔄 **ContextCompressorCore.py** - Context compression
    - Issue: May have encoding dependencies
    - Fix: Ensure pure compression logic

### Development Tools (src/logic/agents/development/core/)
23. 🔄 **BashCore.py** - Bash script linting
    - Issue: subprocess calls
    - Fix: Extract validation logic only
    - Note: Already has context recording added

24. 🔄 **AndroidCore.py** - ADB command logic
    - Issue: subprocess calls
    - Fix: Extract command building logic
    - Note: Already has context recording added

25. 🔄 **ToolDraftingCore.py** - Tool synthesis logic
    - Issue: Unknown dependencies
    - Fix: Review and extract pure logic

### System Cores (src/logic/agents/system/core/)
26. 🔄 **EntropyCore.py** - Entropy calculations
    - Issue: Unknown dependencies
    - Rust benefit: Fast entropy computation

27. 🔄 **ConfigHygieneCore.py** - Config validation
    - Issue: File I/O likely
    - Fix: Extract validation logic

28. 🔄 **CurationCore.py** - Content curation scoring
    - Issue: Unknown dependencies
    - Fix: Review and extract

29. 🔄 **ConvergenceCore.py** (system) - Convergence detection
    - Issue: May overlap with base ConvergenceCore
    - Fix: Consolidate or differentiate

30. 🔄 **ModelRegistryCore.py** - Model registration logic
    - Issue: Likely has I/O
    - Fix: Extract registry operations logic

31. 🔄 **MorphologyCore.py** - Agent morphology
    - Issue: Unknown
    - Fix: Review

32. 🔄 **MultiModalCore.py** - Multi-modal processing
    - Issue: Unknown
    - Fix: Review

### Intelligence & Research (src/logic/agents/intelligence/)
33. 🔄 **LocalizationCore.py** - Localization logic
    - Issue: Unknown
    - Fix: Review

34. 🔄 **SearchMeshCore.py** - Search mesh algorithms
    - Issue: Unknown
    - Fix: Review

35. 🔄 **SynthesisCore.py** - Synthesis logic
    - Issue: Unknown (exec usage noted in scan)
    - Fix: Remove exec, extract pure logic

36. 🔄 **SearchCore.py** - Search algorithms
    - Issue: Likely has API calls
    - Fix: Extract ranking/scoring logic

37. 🔄 **ResearchCore.py** - Research logic
    - Issue: Likely has API calls
    - Fix: Extract analysis logic

38. 🔄 **WebCore.py** - Web scraping logic
    - Issue: Network I/O
    - Fix: Extract parsing/analysis only

### Observability (src/observability/)
39. 🔄 **LoggingCore.py** - Logging utilities
    - Issue: File I/O
    - Fix: Extract formatting/filtering logic

### Infrastructure (src/infrastructure/)
40. 🔄 **AttributionCore.py** - Attribution calculations
    - Issue: Unknown
    - Fix: Review

41. 🔄 **EconomyCore.py** - Economy calculations
    - Issue: Unknown
    - Fix: Review

42. 🔄 **LoadBalancerCore.py** - Load balancing logic
    - Issue: Unknown
    - Fix: Review

43. 🔄 **GPUMonitorCore.py** - GPU metrics
    - Issue: System calls likely
    - Fix: Extract calculation logic

---

## TIER 3: NEEDS WORK (Refactoring Required) (30+ files)

### Complex Agents with I/O
44. ⚠️ **CoderCore.py** - Code generation
    - Issue: Heavy LLM interaction
    - Fix: Extract validation/analysis logic only

45. ⚠️ **CodeQualityCore.py** - Code quality checks
    - Issue: File I/O, subprocess
    - Fix: Extract scoring algorithms

46. ⚠️ **DependencyCore.py** (both versions) - Dependency analysis
    - Issue: File I/O for requirements
    - Fix: Extract parsing/resolution logic
    - Note: Already has context recording added

47. ⚠️ **SecurityCore.py** - Security scanning
    - Issue: Pattern detection on files
    - Fix: Extract pattern matching logic

48. ⚠️ **TechDebtCore.py** - Tech debt analysis
    - Issue: File scanning
    - Fix: Extract scoring logic

49. ⚠️ **DocGenCore.py** - Documentation generation
    - Issue: File I/O
    - Fix: Extract formatting logic

50. ⚠️ **ArchCore.py** - Architecture analysis
    - Issue: File I/O
    - Fix: Extract graph analysis

### Cognitive & Learning
51. ⚠️ **VisionCore.py** - Vision processing
    - Issue: TODO comment - needs implementation
    - Fix: Implement + extract pure vision logic

52. ⚠️ **TheoryOfMindCore.py** - Theory of mind
    - Issue: Unknown complexity
    - Fix: Review

53. ⚠️ **QuantumCore.py** - Quantum algorithms
    - Issue: Unknown complexity
    - Fix: Review

54. ⚠️ **MetacognitiveCore.py** - Metacognition
    - Issue: Unknown
    - Fix: Review

55. ⚠️ **MemoryConsolidatorCore.py** - Memory consolidation
    - Issue: Likely has I/O
    - Fix: Extract consolidation algorithms

56. ⚠️ **LocalRAGCore.py** - Local RAG
    - Issue: Vector DB operations
    - Fix: Extract embedding/search logic

57. ⚠️ **InterpretableCore.py** - Interpretability
    - Issue: Unknown
    - Fix: Review

58. ⚠️ **EvolutionCore.py** - Evolution algorithms
    - Issue: Unknown (perform_specialized_task missing type hints)
    - Fix: Add types, extract pure evolution logic

### Fleet & Orchestration
59. ⚠️ **FleetCore.py** - Fleet management
    - Issue: Heavy I/O and orchestration
    - Fix: Extract coordination algorithms

60. ⚠️ **FleetExecutionCore.py** - Fleet execution
    - Issue: Execution + I/O
    - Fix: Extract scheduling logic

61. ⚠️ **OrchestratorRegistryCore.py** - Orchestrator registry
    - Issue: Registry I/O
    - Fix: Extract lookup logic

62. ⚠️ **ScalingCore.py** - Auto-scaling
    - Issue: System metrics
    - Fix: Extract scaling algorithms

63. ⚠️ **KnowledgeTransferCore.py** - Knowledge transfer
    - Issue: Network + storage
    - Fix: Extract transfer protocols

64. ⚠️ **IntelligenceCore.py** - Collective intelligence
    - Issue: Complex coordination
    - Fix: Extract aggregation logic

65. ⚠️ **ConsensusCore.py** - Consensus algorithms
    - Issue: Network coordination
    - Fix: Extract consensus math

66. ⚠️ **BlackboardCore.py** - Blackboard pattern
    - Issue: Shared state management
    - Fix: Extract pattern matching

67. ⚠️ **TaskDecomposerCore.py** - Task decomposition
    - Issue: Complex AI logic
    - Fix: Extract decomposition algorithms

68. ⚠️ **SelfHealingCore.py** - Self-healing
    - Issue: System interaction
    - Fix: Extract healing strategies

69. ⚠️ **PluginSynthesisCore.py** - Plugin synthesis
    - Issue: Code generation
    - Fix: Extract template logic

70. ⚠️ **ToolCore.py** - Tool management
    - Issue: Tool execution
    - Fix: Extract tool discovery

71. ⚠️ **SignalCore.py** - Signal handling
    - Issue: Event coordination
    - Fix: Extract signal logic

### Other Infrastructure
72. ⚠️ **SandboxCore.py** - Sandbox execution
    - Issue: Process management
    - Fix: Extract validation logic

73. ⚠️ **SimulationCore.py** - Simulation
    - Issue: Complex state management
    - Fix: Extract simulation math

74. ⚠️ **ImportHealerCore.py** - Import healing
    - Issue: AST manipulation + I/O
    - Fix: Extract import resolution logic

75. ⚠️ **LogRotationCore.py** - Log rotation
    - Issue: File I/O
    - Fix: Extract rotation algorithms

76. ⚠️ **RebirthCore.py** - Agent rebirth
    - Issue: Unknown
    - Fix: Review

77. ⚠️ **PoolingCore.py** - Connection pooling
    - Issue: Network management
    - Fix: Extract pooling algorithms

78. ⚠️ **GatewayCore.py** - API gateway
    - Issue: HTTP handling
    - Fix: Extract routing logic

79. ⚠️ **APICore.py** - API logic
    - Issue: HTTP/REST
    - Fix: Extract validation

80. ⚠️ **InterfaceSyncCore.py** - Interface sync
    - Issue: Unknown
    - Fix: Review

---

## CONVERSION PRIORITY MATRIX

### CRITICAL (Start Here)
1. **FormulaEngineCore.py** - Most computational, pure logic ⭐⭐⭐
2. **ErrorMappingCore.py** - Used everywhere, simple ⭐⭐⭐
3. **BenchmarkCore.py** - Performance testing should be fast ⭐⭐⭐
4. **TokenCostCore.py** - Called frequently ⭐⭐
5. **StabilityCore.py** - Core fleet health ⭐⭐
6. **TracingCore.py** - Low-latency requirement ⭐⭐

### HIGH VALUE (Next Wave)
7. ProfilingCore.py
8. ModelFallbackCore.py
9. AutonomyCore.py
10. DeduplicationCore.py
11. ByzantineCore.py
12. AuctionCore.py

### MEDIUM VALUE (After Core)
- All Tier 1 remaining files
- Tier 2 files after cleanup

### FUTURE (Complex Refactoring Required)
- Tier 3 files requiring significant decomposition

---

## RUST CONVERSION CHECKLIST

For each file marked ✅ READY:
- [ ] Verify no hidden I/O operations
- [ ] Check all dependencies are Rust-compatible
- [ ] Add comprehensive type hints in Python version
- [ ] Write property-based tests
- [ ] Create Rust equivalent with PyO3 bindings
- [ ] Benchmark Python vs Rust
- [ ] Add to rust_core module
- [ ] Update Python imports to use Rust version
- [ ] Validate no performance regression
- [ ] Document conversion in ARCHITECTURE.md

---

## ESTIMATED PERFORMANCE GAINS

Based on typical Rust vs Python benchmarks:

| File | Type | Expected Speedup | Impact |
|------|------|------------------|--------|
| FormulaEngineCore.py | CPU-intensive math | 10-50x | CRITICAL |
| TokenCostCore.py | Repeated calculations | 5-20x | HIGH |
| BenchmarkCore.py | Statistical analysis | 10-30x | HIGH |
| StabilityCore.py | Scoring algorithms | 5-15x | HIGH |
| TracingCore.py | High-frequency calls | 3-10x | MEDIUM |
| ErrorMappingCore.py | Simple lookups | 2-5x | LOW |
| DeduplicationCore.py | Hash operations | 5-15x | MEDIUM |

---

## TOTAL SUMMARY

- **Tier 1 (Ready)**: 18 files
- **Tier 2 (Near-ready)**: 25 files
- **Tier 3 (Needs work)**: 30+ files
- **Total Core files identified**: 94

**Recommended First Phase**: Convert Tier 1 files (18 files, ~1500 lines total)
**Expected overall performance gain**: 20-40% for computation-heavy workloads
**Estimated development time**: 2-3 weeks for first phase
