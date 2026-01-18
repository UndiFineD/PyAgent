# Rust Conversion Readiness - PyAgent Core Modules

This document tracks Python files that are ready or nearly ready for Rust conversion. These files typically contain pure logic, minimal I/O, clear interfaces, and high computational value.

**Last Updated**: January 17, 2026 (Phase 17 Complete)
**Total Accelerated Functions**: 111

## Status Legend
- ✅ **OPTIMIZED** - Already integrated with rust_core (PyO3)
- 🚀 **READY** - Pure logic, no I/O, well-typed, ready for conversion
- 🔄 **NEAR-READY** - Minimal I/O or dependencies, needs minor cleanup
- ⚠️ **NEEDS-WORK** - Has I/O or complex dependencies, requires refactoring first
- 📊 **HIGH-VALUE** - Performance-critical, would benefit most from Rust

---

## 📊 FUNCTION INVENTORY (72 Total)

### Security Module (8 functions)
| Function | Purpose |
|----------|---------|
| `scan_code_vulnerabilities_rust` | Scan code for security vulnerabilities |
| `scan_injections_rust` | Detect injection attack patterns |
| `scan_pii_rust` | Find personally identifiable information |
| `analyze_thought_rust` | Analyze agent thought patterns |
| `scan_hardcoded_secrets_rust` | Find hardcoded secrets/credentials |
| `scan_insecure_patterns_rust` | Detect insecure coding patterns |
| `scan_optimization_patterns_rust` | Find optimization opportunities |
| `scan_secrets_rust` | General secrets scanning |

### Statistics Module (4 functions)
| Function | Purpose |
|----------|---------|
| `calculate_pearson_correlation` | Compute Pearson correlation coefficient |
| `predict_linear` | Linear prediction extrapolation |
| `predict_with_confidence_rust` | Predictions with confidence intervals |
| `aggregate_score_rust` | Aggregate compliance scores |

### Neural Module (1 function)
| Function | Purpose |
|----------|---------|
| `cluster_interactions_rust` | Cluster agent interactions |

### Base Module (1 function)
| Function | Purpose |
|----------|---------|
| `is_response_valid_rust` | Validate response content |

### Text Processing Module (58 functions)

#### Core Text Operations
| Function | Purpose |
|----------|---------|
| `tokenize_and_index_rust` | Tokenize and build inverted index |
| `tokenize_query_rust` | Tokenize search queries |
| `calculate_text_similarity_rust` | Jaccard text similarity |
| `find_similar_pairs_rust` | Find similar text pairs |
| `bulk_tokenize_rust` | Batch tokenization |
| `word_frequencies_rust` | Calculate word frequencies |
| `deduplicate_strings_rust` | Deduplicate string collections |

#### Pattern Matching
| Function | Purpose |
|----------|---------|
| `match_patterns_rust` | Match against pattern list |
| `bulk_match_patterns_rust` | Batch pattern matching |
| `check_suppression_rust` | Check suppression patterns |
| `scan_lines_multi_pattern_rust` | Multi-pattern line scanner |
| `apply_patterns_rust` | Apply pattern transformations |
| `analyze_security_patterns_rust` | Security pattern analysis |

#### Search & Filtering
| Function | Purpose |
|----------|---------|
| `search_content_scored_rust` | Scored content search |
| `search_with_tags_rust` | Tag-based search |
| `filter_memory_by_query_rust` | Memory filtering |
| `search_blocks_rust` | Block-based search |

#### Vector Operations
| Function | Purpose |
|----------|---------|
| `cosine_similarity_rust` | Cosine similarity calculation |
| `batch_cosine_similarity_rust` | Batch cosine similarity |
| `find_strong_correlations_rust` | Find correlated vectors |

#### Code Analysis
| Function | Purpose |
|----------|---------|
| `extract_versions_rust` | Extract version strings |
| `batch_scan_files_rust` | Batch file scanning |
| `find_dependents_rust` | Find module dependents |
| `match_policies_rust` | Policy pattern matching |
| `calculate_coupling_rust` | Calculate module coupling |
| `topological_sort_rust` | Topological sort for dependencies |
| `count_untyped_functions_rust` | Count untyped functions |
| `build_graph_edges_rust` | Build dependency graph edges |
| `find_duplicate_code_rust` | Find duplicate code blocks |
| `check_style_patterns_rust` | Check style guide compliance |
| `scan_compliance_patterns_rust` | Scan for compliance issues |
| `analyze_tech_debt_rust` | Analyze technical debt |

#### Infrastructure Operations
| Function | Purpose |
|----------|---------|
| `partition_to_shards_rust` | Partition data to shards |
| `linear_forecast_rust` | Linear time series forecast |
| `normalize_and_hash_rust` | Normalize and hash content |
| `generate_unified_diff_rust` | Generate unified diffs |
| `calculate_jaccard_set_rust` | Jaccard set similarity |
| `fast_cache_key_rust` | Fast cache key generation |
| `fast_prefix_key_rust` | Fast prefix-based key |
| `select_best_agent_rust` | Select optimal agent |
| `aggregate_file_metrics_rust` | Aggregate file metrics |

#### Phase 12: Healing & Resilience
| Function | Purpose |
|----------|---------|
| `calculate_weighted_load_rust` | Calculate weighted load metrics |
| `detect_failed_agents_rust` | Detect failed agents |
| `calculate_variance_rust` | Calculate statistical variance |
| `validate_semver_rust` | Validate semantic versioning |
| `analyze_failure_strategy_rust` | Analyze failure recovery strategy |

#### Phase 13: Stats & Knowledge
| Function | Purpose |
|----------|---------|
| `calculate_sum_rust` | Fast sum calculation |
| `calculate_avg_rust` | Fast average calculation |
| `calculate_min_rust` | Fast minimum finding |
| `calculate_max_rust` | Fast maximum finding |
| `calculate_median_rust` | Fast median (P50) |
| `calculate_p95_rust` | 95th percentile |
| `calculate_p99_rust` | 99th percentile |
| `calculate_stddev_rust` | Standard deviation |
| `calculate_pearson_correlation_rust` | Pearson correlation (new) |
| `calculate_shard_id_rust` | Adler32 hash sharding |
| `merge_knowledge_rust` | JSON dict merging |
| `filter_stable_knowledge_rust` | Confidence filtering |

#### Phase 17: vLLM-Inspired Utilities (11 functions)
| Function | Purpose |
|----------|---------|
| `cdiv_rust` | Ceiling division without floating point |
| `next_power_of_2_rust` | Smallest power of 2 >= n |
| `prev_power_of_2_rust` | Largest power of 2 <= n |
| `round_up_rust` | Round up to nearest multiple |
| `round_down_rust` | Round down to nearest multiple |
| `atomic_counter_add_rust` | Atomic counter addition |
| `xxhash_rust` | Fast non-cryptographic hashing |
| `fast_cache_hash_rust` | Cache key hashing with prefix |
| `cache_hit_ratio_rust` | Calculate cache hit ratio |
| `batch_cdiv_rust` | Batch ceiling division |
| `batch_next_power_of_2_rust` | Batch power-of-2 calculation |

---

## TIER 1: OPTIMIZED (72 files/functions)

### Core Infrastructure
1. ✅ **SecurityCore.py** - Integrated with scan_code_vulnerabilities_rust, scan_injections_rust
2. ✅ **ObservabilityCore.py** - Integrated with calculate_pearson_correlation, predict_linear
3. ✅ **ReportSearchEngine.py** - Integrated with tokenize_and_index_rust, search_content_scored_rust
4. ✅ **MergeDetector.py** - Integrated with calculate_text_similarity_rust, find_similar_pairs_rust
5. ✅ **SuppressionEngine.py** - Integrated with check_suppression_rust, scan_lines_multi_pattern_rust
6. ✅ **PrivacyCore.py** - Integrated with scan_pii_rust
7. ✅ **DependencyCore.py** - Integrated with find_dependents_rust, calculate_coupling_rust
8. ✅ **PolicyCore.py** - Integrated with match_policies_rust
9. ✅ **QuantumShardOrchestrator.py** - Integrated with partition_to_shards_rust
10. ✅ **TypeCoverageCore.py** - Integrated with count_untyped_functions_rust
11. ✅ **ModuleGraphCore.py** - Integrated with build_graph_edges_rust, topological_sort_rust

### Agent Logic
12. ✅ **CoderCore.py** - Integrated with check_style_patterns_rust, find_duplicate_code_rust
13. ✅ **ComplianceCore.py** - Integrated with scan_compliance_patterns_rust
14. ✅ **LessonCore.py** - Integrated with normalize_and_hash_rust
15. ✅ **DiffGenerator.py** - Integrated with generate_unified_diff_rust
16. ✅ **MorphologyCore.py** - Integrated with calculate_jaccard_set_rust
17. ✅ **ResponseCache.py** - Integrated with fast_cache_key_rust, fast_prefix_key_rust
18. ✅ **LoadBalancerCore.py** - Integrated with select_best_agent_rust
19. ✅ **EntropyCore.py** - Integrated with aggregate_file_metrics_rust
20. ✅ **ScalingCore.py** - Integrated with calculate_weighted_load_rust
21. ✅ **SelfHealingCore.py** - Integrated with detect_failed_agents_rust, validate_semver_rust
22. ✅ **StabilityCore.py** - Integrated with calculate_variance_rust
23. ✅ **SelfHealingEngineCore.py** - Integrated with analyze_failure_strategy_rust
24. ✅ **TechDebtCore.py** - Integrated with analyze_tech_debt_rust

### Stats & Metrics
25. ✅ **MetricsCore.py (StatsRollupCore)** - Integrated with calculate_sum/avg/min/max/median/stddev_rust
26. ✅ **MetricsCore.py (CorrelationCore)** - Integrated with calculate_pearson_correlation_rust
27. ✅ **ShardedKnowledgeCore.py** - Integrated with calculate_shard_id_rust, merge_knowledge_rust

### Previous Phases (1-9)
28-72. ✅ **[Previous 44 files]** - See Phase 1-9 documentation

---

## 🔧 PROFILING TOOLS

### RustProfiler (New)
Location: `src/observability/profiling/RustProfiler.py`

**Features:**
- Real-time call tracking with nanosecond precision
- Thread-safe singleton design
- Python fallback detection
- Source location tracking
- JSON report export

**Usage:**
```python
from src.observability.profiling.RustProfiler import RustProfiler, RustUsageScanner

# Get profiler instance
profiler = RustProfiler.get_instance()

# Scan codebase for Rust usage
scanner = RustUsageScanner()
report = scanner.generate_report(Path("src"), Path("tests"))

# Print runtime statistics
profiler.print_report()
```

**CLI Usage:**
```bash
python src/observability/profiling/RustProfiler.py --src src --tests tests -o report.json -v
```

---

## TIER 2: READY FOR CONVERSION (0 files)

(All Tier 2 candidates migrated to Tier 1/Optimized)

---

## TIER 3: NEAR-READY (Needs Minor Cleanup)

| File | Reason | Blocker |
|------|--------|---------|
| `ContextBuilderCore.py` | Text processing heavy | Needs prompt_path I/O separation |
| `FederatedSearchCore.py` | Result aggregation | Has rust_core fallback, needs full integration |

---

## 📈 MIGRATION HISTORY

| Phase | Date | Functions Added | Total |
|-------|------|-----------------|-------|
| 1-9 | Dec 2025 | 43 | 43 |
| 10 | Jan 10, 2026 | 5 | 48 |
| 11 | Jan 12, 2026 | 6 | 54 |
| 12 | Jan 14, 2026 | 6 | 60 |
| 13 | Jan 16, 2026 | 12 | 72 |
| 14 | Jan 17, 2026 | 8 | 80 |
| 15 | Jan 17, 2026 | 8 | 88 |
| 16 | Jan 17, 2026 | 12 | 100 |

---

## 📊 PHASE 14: COGNITIVE & BUFFER ACCELERATION (8 Functions)

| Function | Purpose | Module |
|----------|---------|--------|
| `count_hedge_words_rust` | Multi-pattern hedge word detection | MetacognitiveCore |
| `predict_intent_rust` | Pattern-based intent classification | MetacognitiveCore |
| `top_k_indices_rust` | O(n) top-K selection for activations | InterpretableCore |
| `decompose_activations_rust` | Vectorized SAE decomposition | InterpretableCore |
| `sort_buffer_by_priority_rust` | Priority-timestamp composite sorting | AttentionBufferAgent |
| `filter_stale_entries_rust` | Timestamp-based entry filtering | AttentionBufferAgent |
| `calculate_statistical_significance` | T-test significance calculation | ABTestCore |
| `calculate_sample_size` | Power analysis sample size | ABTestCore |

---

## 📊 PHASE 15: CORE & INFRASTRUCTURE ACCELERATION (8 Functions)

| Function | Purpose | Module |
|----------|---------|--------|
| `analyze_structure_rust` | Fast line/word/token counting | AgentCore |
| `estimate_tokens_rust` | BPE-approximated token estimation | SubagentRunner |
| `detect_cycles_rust` | DFS-based cycle detection in graphs | AgentRegistryCore |
| `validate_response_rust` | Vectorized content validation | SubagentRunner |
| `process_text_rust` | Fast text normalization | AgentCore |
| `exponential_forecast_rust` | Exponential smoothing forecasts | ObservabilityCore |
| `batch_token_count_rust` | Batch token counting | ExecutionEngine |
| `graph_bfs_rust` | BFS graph traversal | DependencyCore |

---

## 🎯 NEXT TARGETS (Phase 17+)

1. **ContextBuilder** - Context window pruning and optimization
2. **FederatedSearch** - Distributed search aggregation
3. **WorkflowEngine** - Workflow state machine transitions
4. **MetricAggregator** - Real-time metric aggregation
5. **GraphContextEngine** - Graph traversal and pathfinding

---

## 📊 PHASE 16: VECTOR MATH & AGGREGATION (12 Functions)

| Function | Purpose | Module |
|----------|---------|--------|
| `compute_embedding_stats_rust` | Mean, variance, norm, sparsity, percentiles | DimensionalityAgent |
| `kmeans_cluster_rust` | K-means clustering with iterative refinement | DimensionalityAgent |
| `compute_similarity_matrix_rust` | Cosine similarity matrix with top-K pairs | DimensionalityAgent |
| `pca_reduce_rust` | PCA-like dimensionality reduction | DimensionalityAgent |
| `random_projection_rust` | Random projection for dimension reduction | DimensionalityAgent |
| `compress_json_rust` | JSON serialization + zlib compression | StorageEngine |
| `decompress_json_rust` | Zlib decompression + JSON parsing | StorageEngine |
| `weighted_random_select_rust` | Weighted random selection for A/B testing | PromptManagers |
| `keyword_search_score_rust` | Batch keyword matching with scoring | SemanticSearchEngine |
| `calculate_ttest_rust` | Welch's t-test for A/B significance | ABEngine |
| `batch_aggregate_rust` | Batch aggregation (sum/avg/min/max) | RollupEngine |
| `rolling_window_rust` | Rolling window statistics | RollupEngine |
