# PyAgent vLLM Integration Roadmap: Phases 46-55

**Created**: January 18, 2026  
**Current State**: 486 Rust functions, ~136 Python modules, ~2933 tests  
**Goal**: Complete vLLM v1 pattern coverage and exceed with PyAgent innovations

---

## Executive Summary

This roadmap covers the next 10 phases of vLLM integration, focusing on:
1. **Structured Output Backends** (Phase 46-47)
2. **Attention Backends** (Phase 48-49)
3. **Speculative Decoding v3** (Phase 50-51)
4. **Worker & Memory Management** (Phase 52-53)
5. **Async Engine & Coordination** (Phase 54-55)

---

## Phase 46: XGrammar & Structured Output Backends ✨ PRIORITY
**Focus**: Complete structured output backend ecosystem

### Modules to Implement
1. **XGrammarBackend.py** (~600 lines)
   - GrammarCompiler wrapper
   - TokenizerInfo integration
   - Bitmask allocation
   - JSON schema compilation
   - Regex/EBNF/Structural tag support

2. **GuidanceBackend.py** (~500 lines)
   - Guidance library integration
   - Async grammar compilation
   - Stateful token tracking
   - Template-based generation

3. **LMFormatEnforcerBackend.py** (~450 lines)
   - JSON schema enforcement
   - Regex pattern enforcement
   - Character-level constraints
   - Fast bitmask generation

4. **LogitsProcessorV2.py** (~550 lines)
   - BatchUpdate interface
   - MoveDirectionality enum
   - State update lifecycle
   - Argmax invariance tracking

5. **BadWordsProcessorV2.py** (~400 lines)
   - N-gram bad word matching
   - Draft token support
   - Batch-level filtering
   - Streaming integration

6. **StructuredOutputOrchestrator.py** (~500 lines)
   - Multi-backend fallback
   - Grammar caching
   - Bitmask pooling
   - Performance metrics

### Rust Accelerations (~15 functions)
- xgrammar_bitmask_fill_rust
- grammar_cache_key_rust
- batch_update_indices_rust
- bad_words_match_ngram_rust
- logit_bias_apply_rust
- min_p_threshold_rust
- structural_tag_parse_rust
- regex_dfa_transition_rust

### Tests (~50)
- XGrammar compilation, bitmask generation
- Guidance template rendering
- LMFormatEnforcer constraint application
- BatchUpdate state transitions
- Bad words n-gram matching

---

## Phase 47: Advanced Logits Processors
**Focus**: Complete logits processor ecosystem

### Modules to Implement
1. **MinPLogitsProcessor.py** - Dynamic probability thresholding
2. **LogitBiasProcessor.py** - Token-level bias application
3. **DryRunProcessor.py** - Dry run repetition penalty
4. **XTCProcessor.py** - Exclude top choices sampling
5. **PresencePenaltyProcessor.py** - Presence-based penalty
6. **FrequencyPenaltyProcessor.py** - Frequency-based penalty

### Rust Accelerations (~12 functions)
- min_p_filter_rust
- logit_bias_sparse_rust
- dry_run_penalty_rust
- xtc_sampling_rust
- presence_frequency_combined_rust

### Tests (~40)
- Each processor type with edge cases
- Composition and chaining
- Batch processing efficiency

---

## Phase 48: FlexAttention & Tree Attention
**Focus**: Advanced attention backends

### Modules to Implement
1. **FlexAttentionBackend.py** (~650 lines)
   - PyTorch 2.5+ flex_attention API
   - Block mask generation
   - Custom score mod functions
   - Nested tensor support

2. **TreeAttentionBackend.py** (~600 lines)
   - Tree-structured attention masks
   - Speculation tree support
   - Branch-aware scoring
   - Verification acceleration

3. **LinearAttentionBackend.py** (~500 lines)
   - Linear complexity attention
   - Feature map transformations
   - Causal masking
   - Recurrent form support

4. **GDNAttention.py** (~450 lines)
   - Gaussian distribution networks
   - Probabilistic attention
   - Uncertainty estimation

### Rust Accelerations (~14 functions)
- flex_attention_mask_rust
- tree_attention_paths_rust
- linear_attention_feature_rust
- attention_score_mod_rust

### Tests (~45)
- FlexAttention with custom masks
- Tree attention verification paths
- Linear attention convergence

---

## Phase 49: MLA & Mamba Attention Variants
**Focus**: Advanced attention architectures

### Modules to Implement
1. **MLAAttentionV2.py** - Multi-Latent Attention improvements
2. **Mamba1AttentionBackend.py** - Mamba 1.0 integration
3. **Mamba2AttentionBackend.py** - Mamba 2.0 SSD
4. **ShortConvAttention.py** - Short convolution layers
5. **AttentionRegistryV2.py** - Unified backend registry

### Rust Accelerations (~10 functions)
- mla_kv_compress_v2_rust
- mamba_selective_scan_rust
- short_conv_rust
- attention_registry_lookup_rust

### Tests (~35)
- MLA head configuration
- Mamba state management
- Registry hot-swapping

---

## Phase 50: EAGLE Speculative v2
**Focus**: Complete EAGLE proposer implementation

### Modules to Implement
1. **EagleProposerV2.py** (~700 lines)
   - EAGLE-1 and EAGLE-2 support
   - Tree attention integration
   - Draft model management
   - Multi-modal support (EAGLE3)

2. **EagleAttentionBuilder.py** (~500 lines)
   - Tree attention metadata
   - Draft indexer metadata
   - Position tracking

3. **EagleCUDAGraph.py** (~450 lines)
   - CUDA graph capture for EAGLE
   - Piecewise compilation
   - Buffer management

4. **EagleVerifier.py** (~400 lines)
   - Tree verification
   - Acceptance tracking
   - Statistics collection

### Rust Accelerations (~12 functions)
- eagle_tree_build_rust
- eagle_verify_path_rust
- eagle_draft_buffer_rust
- eagle_cuda_prepare_rust

### Tests (~40)
- EAGLE tree construction
- Multi-path verification
- CUDA graph integration

---

## Phase 51: Suffix Decoding & Advanced Speculation
**Focus**: Suffix tree-based speculation

### Modules to Implement
1. **SuffixDecodingProposer.py** (~600 lines)
   - Suffix tree construction
   - Pattern matching
   - Speculation limits
   - Cache management

2. **SuffixDecodingCache.py** (~500 lines)
   - Request-level suffix trees
   - Eviction policies
   - Active/cached request states

3. **SpecDecodeMetricsV2.py** (~400 lines)
   - Acceptance rate tracking
   - Latency breakdown
   - Token savings calculation

4. **SpecDecodeConfig.py** (~350 lines)
   - Method selection (Eagle/Medusa/Suffix)
   - Tuning parameters
   - Auto-detection

### Rust Accelerations (~10 functions)
- suffix_tree_build_rust
- suffix_match_longest_rust
- suffix_cache_evict_rust
- spec_metrics_aggregate_rust

### Tests (~35)
- Suffix tree operations
- Cache eviction
- Metrics accuracy

---

## Phase 52: WorkspaceManager & Memory Optimization
**Focus**: DBO workspace and memory management

### Modules to Implement
1. **WorkspaceManager.py** (~600 lines)
   - DBO workspace allocation
   - Simultaneous tensor views
   - Lock-based growth control
   - Memory debugging

2. **UBatchingUtils.py** (~500 lines)
   - Micro-batch slicing
   - Thread coordination
   - Event synchronization
   - SM management

3. **MemoryProfiler.py** (~450 lines)
   - Peak memory tracking
   - Allocation patterns
   - Fragmentation analysis

4. **BufferRecycler.py** (~400 lines)
   - Buffer reuse pools
   - Size-class allocation
   - Reference counting

### Rust Accelerations (~12 functions)
- workspace_size_compute_rust
- ubatch_slice_optimal_rust
- memory_profile_rust
- buffer_recycle_rust

### Tests (~40)
- Workspace allocation patterns
- UBatch coordination
- Memory profiling accuracy

---

## Phase 53: BlockTable & KV Management V2
**Focus**: Advanced block management

### Modules to Implement
1. **BlockTableV2.py** (~650 lines)
   - Hybrid block size support
   - Context parallel integration
   - Slot mapping optimization
   - PCP/DCP awareness

2. **KVCacheInterfaceV2.py** (~550 lines)
   - Multi-group management
   - Dynamic block allocation
   - Hierarchical caching

3. **BlockHashManager.py** (~400 lines)
   - Content-based block hashing
   - Prefix cache integration
   - Hash collision handling

### Rust Accelerations (~10 functions)
- block_table_append_rust
- slot_mapping_batch_rust
- block_hash_compute_rust
- kv_block_transfer_rust

### Tests (~35)
- Block table operations
- Hybrid block sizes
- Hash-based deduplication

---

## Phase 54: AsyncScheduler & Engine V2
**Focus**: Asynchronous scheduling patterns

### Modules to Implement
1. **AsyncSchedulerV2.py** (~700 lines)
   - Async update after schedule
   - Output placeholder tracking
   - Speculative token handling
   - Structured output integration

2. **SchedulerOutput.py** (~500 lines)
   - Complete output structure
   - Spec decode tokens
   - Pending structured output

3. **RequestQueueV2.py** (~450 lines)
   - Priority-based async queue
   - Deadline-aware scheduling
   - Fair share policies

4. **EngineCoordinator.py** (~550 lines)
   - Engine lifecycle management
   - Error recovery
   - Graceful shutdown

### Rust Accelerations (~12 functions)
- async_schedule_update_rust
- request_priority_compute_rust
- deadline_urgency_rust
- engine_state_transition_rust

### Tests (~45)
- Async scheduling flow
- Output placeholder management
- Priority queue operations

---

## Phase 55: DPCoordinator & Multi-Node
**Focus**: Data parallel coordination

### Modules to Implement
1. **DPCoordinatorV2.py** (~700 lines)
   - ZMQ-based coordination
   - Request wave tracking
   - Stats publishing
   - External LB integration

2. **DPEngineSync.py** (~500 lines)
   - Engine state synchronization
   - Wave number management
   - Paused/running transitions

3. **MultiNodeExecutor.py** (~550 lines)
   - Cross-node communication
   - Tensor parallel distribution
   - Pipeline parallel support

4. **LoadBalancerClient.py** (~400 lines)
   - P2C selection
   - Weighted round-robin
   - Least connections

### Rust Accelerations (~10 functions)
- dp_stats_aggregate_rust
- wave_sync_check_rust
- load_balance_select_rust
- multi_node_coordinate_rust

### Tests (~40)
- DP coordination flow
- Wave synchronization
- Load balancing accuracy

---

## Summary Table

| Phase | Focus | Modules | Rust Fns | Tests |
|-------|-------|---------|----------|-------|
| 46 | XGrammar & Structured Output | 6 | 15 | 50 |
| 47 | Advanced Logits Processors | 6 | 12 | 40 |
| 48 | FlexAttention & Tree Attention | 4 | 14 | 45 |
| 49 | MLA & Mamba Variants | 5 | 10 | 35 |
| 50 | EAGLE Speculative v2 | 4 | 12 | 40 |
| 51 | Suffix Decoding | 4 | 10 | 35 |
| 52 | WorkspaceManager & Memory | 4 | 12 | 40 |
| 53 | BlockTable & KV v2 | 3 | 10 | 35 |
| 54 | AsyncScheduler & Engine v2 | 4 | 12 | 45 |
| 55 | DPCoordinator & Multi-Node | 4 | 10 | 40 |
| **Total** | - | **44** | **117** | **405** |

---

## Projected Final State

After Phase 55:
- **Rust Functions**: 486 + 117 = **603**
- **Python Modules**: 136 + 44 = **180**
- **Tests**: 2933 + 405 = **3338**
- **vLLM Coverage**: **95%+**

---

## Beyond vLLM Innovations (Planned)

| Feature | Phase | Innovation |
|---------|-------|------------|
| Multi-backend grammar fallback | 46 | Automatic backend selection |
| Adaptive min-p | 47 | Context-aware thresholding |
| Hybrid attention routing | 48 | Auto-switch based on sequence length |
| MLA + Mamba fusion | 49 | Combined state compression |
| EAGLE-3 multimodal | 50 | Vision-language speculation |
| Suffix trie indexing | 51 | Compressed suffix representation |
| Predictive workspace | 52 | Pre-allocation based on batch patterns |
| Hierarchical block tables | 53 | Multi-level block management |
| Speculative async | 54 | Async output token generation |
| Locality-aware DP | 55 | Network topology optimization |
