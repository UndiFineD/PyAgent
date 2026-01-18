// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use pyo3::prelude::*;

mod agents;
mod base;
mod stats;
mod utils;
mod security;
mod neural;
mod text;
mod inference;
mod multimodal;
mod quantlora;

// Imports for wrapping
use agents::*;
use base::*;
use stats::*;
use utils::*;
use neural::*;

/// A Python module implemented in Rust.
#[pymodule]
fn rust_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Agents
    m.add_function(wrap_pyfunction!(calculate_synaptic_weight, m)?)?;
    m.add_function(wrap_pyfunction!(enforce_vram_quota, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_vcg_auction, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_agreement_score, m)?)?;
    m.add_function(wrap_pyfunction!(select_committee, m)?)?;
    m.add_function(wrap_pyfunction!(get_required_quorum, m)?)?;
    m.add_function(wrap_pyfunction!(detect_deviating_hashes, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_bid_priority_score, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_gpu_surcharge, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_consensus_winner, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_new_utility, m)?)?;
    m.add_function(wrap_pyfunction!(filter_relevant_memories, m)?)?;
    m.add_function(wrap_pyfunction!(create_episode_struct, m)?)?;
    m.add_function(wrap_pyfunction!(generate_heuristic_plan, m)?)?;
    m.add_function(wrap_pyfunction!(execute_dcap_cycle, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_paper, m)?)?;
    m.add_function(wrap_pyfunction!(draft_tool_code, m)?)?;
    m.add_function(wrap_pyfunction!(generate_failure_hash, m)?)?;
    m.add_function(wrap_pyfunction!(evaluate_bypass, m)?)?;
    m.add_function(wrap_pyfunction!(filter_relevant_insights, m)?)?;

    // Utils
    m.add_function(wrap_pyfunction!(fast_hash, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_metrics_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_interaction_shard_md5, m)?)?;
    m.add_function(wrap_pyfunction!(evaluate_formula, m)?)?;
    m.add_function(wrap_pyfunction!(compress_python_regex, m)?)?;
    m.add_function(wrap_pyfunction!(summarize_markdown, m)?)?;
    m.add_function(wrap_pyfunction!(parse_bing_results, m)?)?;
    m.add_function(wrap_pyfunction!(parse_google_results, m)?)?;
    m.add_function(wrap_pyfunction!(parse_ddg_results, m)?)?;
    m.add_function(wrap_pyfunction!(format_results_block, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_stochastic_failures, m)?)?;
    m.add_function(wrap_pyfunction!(apply_latency_spike, m)?)?;
    m.add_function(wrap_pyfunction!(format_progress_bar, m)?)?;
    m.add_function(wrap_pyfunction!(score_tool_relevance, m)?)?;
    m.add_function(wrap_pyfunction!(generate_openapi_spec, m)?)?;
    m.add_function(wrap_pyfunction!(flatten_env_vars, m)?)?;
    m.add_function(wrap_pyfunction!(prune_directory_rust, m)?)?;
    m.add_function(wrap_pyfunction!(deep_clean_pycache_rust, m)?)?;
    m.add_function(wrap_pyfunction!(ensure_safety_flags_rust, m)?)?;
    m.add_function(wrap_pyfunction!(parse_adb_devices_rust, m)?)?;

    // Phase 17: vLLM-Inspired Math & Utility Functions
    m.add_function(wrap_pyfunction!(cdiv_rust, m)?)?;
    m.add_function(wrap_pyfunction!(next_power_of_2_rust, m)?)?;
    m.add_function(wrap_pyfunction!(prev_power_of_2_rust, m)?)?;
    m.add_function(wrap_pyfunction!(round_up_rust, m)?)?;
    m.add_function(wrap_pyfunction!(round_down_rust, m)?)?;
    m.add_function(wrap_pyfunction!(atomic_counter_add_rust, m)?)?;
    m.add_function(wrap_pyfunction!(xxhash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(fast_cache_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(cache_hit_ratio_rust, m)?)?;
    m.add_function(wrap_pyfunction!(batch_cdiv_rust, m)?)?;
    m.add_function(wrap_pyfunction!(batch_next_power_of_2_rust, m)?)?;

    // Phase 22: JSONTree Utilities
    m.add_function(wrap_pyfunction!(json_count_leaves_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_iter_leaves_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_flatten_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_depth_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_get_path_rust, m)?)?;
    m.add_function(wrap_pyfunction!(json_validate_leaves_rust, m)?)?;

    // Phase 23: Advanced Serialization & Validation
    m.add_function(wrap_pyfunction!(msgpack_encode_tensor_meta_rust, m)?)?;
    m.add_function(wrap_pyfunction!(validate_tensor_shape_rust, m)?)?;
    m.add_function(wrap_pyfunction!(apply_temperature_rust, m)?)?;
    m.add_function(wrap_pyfunction!(apply_top_k_rust, m)?)?;
    m.add_function(wrap_pyfunction!(apply_repetition_penalty_rust, m)?)?;
    m.add_function(wrap_pyfunction!(compute_logits_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(encode_slice_rust, m)?)?;

    // Phase 24: Advanced Observability & Parsing
    m.add_function(wrap_pyfunction!(structured_counter_diff_rust, m)?)?;
    m.add_function(wrap_pyfunction!(flat_logprobs_append_rust, m)?)?;
    m.add_function(wrap_pyfunction!(extract_json_tool_calls_rust, m)?)?;
    m.add_function(wrap_pyfunction!(dedupe_log_messages_rust, m)?)?;
    m.add_function(wrap_pyfunction!(detect_cloud_provider_rust, m)?)?;
    m.add_function(wrap_pyfunction!(validate_prompt_rust, m)?)?;
    m.add_function(wrap_pyfunction!(parse_xml_tool_call_rust, m)?)?;

    // Base
    m.add_function(wrap_pyfunction!(generate_cache_key, m)?)?;
    m.add_function(wrap_pyfunction!(get_error_code, m)?)?;
    m.add_function(wrap_pyfunction!(get_error_documentation_link, m)?)?;
    m.add_function(wrap_pyfunction!(redact_pii, m)?)?;
    m.add_function(wrap_pyfunction!(identify_blind_spots, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_daemon_sleep_interval, m)?)?;
    m.add_function(wrap_pyfunction!(generate_self_improvement_plan, m)?)?;
    m.add_function(wrap_pyfunction!(generate_challenge, m)?)?;
    m.add_function(wrap_pyfunction!(generate_auth_proof, m)?)?;
    m.add_function(wrap_pyfunction!(verify_auth_proof, m)?)?;
    m.add_function(wrap_pyfunction!(is_proof_expired, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_backoff, m)?)?;
    m.add_function(wrap_pyfunction!(should_attempt_recovery, m)?)?;
    m.add_function(wrap_pyfunction!(evaluate_state_transition, m)?)?;
    m.add_function(wrap_pyfunction!(generate_agent_id, m)?)?;
    m.add_function(wrap_pyfunction!(sign_payload, m)?)?;
    m.add_function(wrap_pyfunction!(verify_signature, m)?)?;
    m.add_function(wrap_pyfunction!(validate_identity, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_decay, m)?)?;
    m.add_function(wrap_pyfunction!(is_in_refractory, m)?)?;
    m.add_function(wrap_pyfunction!(update_weight_on_fire, m)?)?;
    m.add_function(wrap_pyfunction!(should_prune, m)?)?;
    m.add_function(wrap_pyfunction!(verify_fleet_health, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_anchoring_fallback, m)?)?;
    m.add_function(wrap_pyfunction!(check_latent_reasoning, m)?)?;
    m.add_function(wrap_pyfunction!(is_response_valid_rust, m)?)?;

    // Stats
    m.add_function(wrap_pyfunction!(calculate_baseline, m)?)?;
    m.add_function(wrap_pyfunction!(check_regression, m)?)?;
    m.add_function(wrap_pyfunction!(score_efficiency, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_priority_score, m)?)?;
    m.add_function(wrap_pyfunction!(assess_response_quality, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_token_estimate, m)?)?;
    m.add_function(wrap_pyfunction!(deduplicate_entries, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_response, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_token_cost, m)?)?;
    m.add_function(wrap_pyfunction!(select_best_model, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_cyclomatic_complexity, m)?)?;
    m.add_function(wrap_pyfunction!(check_finetuning_trigger, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_pearson_correlation, m)?)?;
    m.add_function(wrap_pyfunction!(predict_linear, m)?)?;
    m.add_function(wrap_pyfunction!(predict_with_confidence_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_p95, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_avg, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_sum, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_min, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_max, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_stddev, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_median, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_stability_score, m)?)?;
    m.add_function(wrap_pyfunction!(is_in_stasis, m)?)?;
    m.add_function(wrap_pyfunction!(get_healing_threshold, m)?)?;
    m.add_function(wrap_pyfunction!(create_span_context, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_latency_breakdown, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_optimization_priority, m)?)?;
    m.add_function(wrap_pyfunction!(identify_bottlenecks, m)?)?;
    m.add_function(wrap_pyfunction!(get_fallback_chain, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_jaccard_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(deduplicate_by_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_statistical_significance, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_sample_size, m)?)?;
    m.add_function(wrap_pyfunction!(audit_content_rust, m)?)?;
    m.add_function(wrap_pyfunction!(aggregate_score_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_superposition_weights, m)?)?;
    m.add_function(wrap_pyfunction!(simulate_interference_pattern, m)?)?;
    m.add_function(wrap_pyfunction!(generate_mermaid_graph, m)?)?;
    m.add_function(wrap_pyfunction!(filter_active_topology_relationships, m)?)?;
    // regex_compress_python replaced by compress_python_regex from utils
    m.add_function(wrap_pyfunction!(compress_python_regex, m)?)?;
    m.add_function(wrap_pyfunction!(summarize_markdown, m)?)?;
    m.add_function(wrap_pyfunction!(generate_synthetic_snippets, m)?)?;
    m.add_function(wrap_pyfunction!(vectorize_text_insight, m)?)?;
    m.add_function(wrap_pyfunction!(average_feature_vectors, m)?)?;
    m.add_function(wrap_pyfunction!(agents::aggregate_search_results, m)?)?;
    m.add_function(wrap_pyfunction!(agents::detect_cultural_issues, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_stats_rollup, m)?)?;
    m.add_function(wrap_pyfunction!(agents::extract_python_symbols, m)?)?;
    m.add_function(wrap_pyfunction!(agents::extract_graph_entities_regex, m)?)?;
    m.add_function(wrap_pyfunction!(agents::extract_markdown_backlinks, m)?)?;
    m.add_function(wrap_pyfunction!(mask_sensitive_logs, m)?)?;
    m.add_function(wrap_pyfunction!(to_snake_case_rust, m)?)?;
    m.add_function(wrap_pyfunction!(build_log_entry_rust, m)?)?;

    // Security
    m.add_function(wrap_pyfunction!(security::analyze_thought_rust, m)?)?;
    m.add_function(wrap_pyfunction!(security::scan_secrets_rust, m)?)?;
    m.add_function(wrap_pyfunction!(security::scan_pii_rust, m)?)?;
    m.add_function(wrap_pyfunction!(security::scan_code_vulnerabilities_rust, m)?)?;
    m.add_function(wrap_pyfunction!(security::scan_injections_rust, m)?)?;
    m.add_function(wrap_pyfunction!(security::scan_optimization_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(security::scan_hardcoded_secrets_rust, m)?)?;
    m.add_function(wrap_pyfunction!(security::scan_insecure_patterns_rust, m)?)?;

    // Neural
    m.add_function(wrap_pyfunction!(cluster_interactions_rust, m)?)?;
    m.add_class::<HardwareProfile>()?;
    m.add_class::<TransformerConfig>()?;
    m.add_class::<NeuralTransformer>()?;
    m.add_class::<FlexibleNeuralNetwork>()?;
    m.add_class::<KVCache>()?;
    m.add_function(wrap_pyfunction!(top_k_cosine_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(vectorize_text_insight, m)?)?;
    m.add_function(wrap_pyfunction!(average_feature_vectors, m)?)?;
    m.add_function(wrap_pyfunction!(generate_synthetic_snippets, m)?)?;

    // Text processing (ReportSearchEngine, MergeDetector)
    m.add_function(wrap_pyfunction!(text::tokenize_and_index_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::tokenize_query_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_text_similarity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::find_similar_pairs_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::bulk_tokenize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::word_frequencies_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::deduplicate_strings_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::match_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::bulk_match_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::check_suppression_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::scan_lines_multi_pattern_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::search_content_scored_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::extract_versions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::batch_scan_files_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::cosine_similarity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::batch_cosine_similarity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::find_strong_correlations_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::search_with_tags_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::filter_memory_by_query_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::find_dependents_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::match_policies_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::search_blocks_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::apply_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::analyze_security_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_coupling_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::topological_sort_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::partition_to_shards_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::count_untyped_functions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::build_graph_edges_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::find_duplicate_code_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::linear_forecast_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::check_style_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::scan_compliance_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::normalize_and_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::generate_unified_diff_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_jaccard_set_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::fast_cache_key_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::fast_prefix_key_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::select_best_agent_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::aggregate_file_metrics_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_weighted_load_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::detect_failed_agents_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_variance_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::validate_semver_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::analyze_failure_strategy_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::analyze_tech_debt_rust, m)?)?;
    // Phase 13: Stats & Knowledge Core
    m.add_function(wrap_pyfunction!(text::calculate_sum_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_avg_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_min_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_max_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_median_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_p95_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_p99_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_stddev_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_pearson_correlation_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::calculate_shard_id_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::merge_knowledge_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::filter_stable_knowledge_rust, m)?)?;
    // Phase 14: SelfImprovementCore Acceleration
    m.add_function(wrap_pyfunction!(text::analyze_code_quality_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::prepare_debt_records_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::apply_simple_fixes_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::bulk_replace_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::bulk_replace_files_rust, m)?)?;
    m.add_function(wrap_pyfunction!(text::scan_workspace_quality_rust, m)?)?;

    m.add_class::<CoderCore>()?;
    m.add_class::<ToolDraftingCore>()?;
    m.add_class::<WebCore>()?;
    m.add_class::<CodeQualityCore>()?;

    // Neural & Transformer
    m.add_class::<HardwareProfile>()?;
    m.add_class::<TransformerConfig>()?;
    m.add_class::<NeuralTransformer>()?;
    m.add_class::<FlexibleNeuralNetwork>()?;
    m.add_class::<KVCache>()?;
    m.add_class::<GenerationStats>()?;
    m.add_function(wrap_pyfunction!(cluster_interactions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(top_k_cosine_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(generate_neural_response, m)?)?;
    m.add_function(wrap_pyfunction!(vectorize_text_insight, m)?)?;
    m.add_function(wrap_pyfunction!(vectorize_text_insight_with_stats, m)?)?;
    m.add_function(wrap_pyfunction!(average_feature_vectors, m)?)?;
    m.add_function(wrap_pyfunction!(generate_synthetic_snippets, m)?)?;
    m.add_function(wrap_pyfunction!(generate_synthetic_snippets_with_stats, m)?)?;

    // Phase 25: Inference Acceleration (Speculative Decoding, Prefix Cache, KV Cache)
    m.add_function(wrap_pyfunction!(inference::ngram_match_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::build_ngram_index_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::find_continuations_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::build_suffix_array_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::suffix_search_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_block_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_block_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::lru_evict_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::lfu_evict_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::optimize_block_copy_order_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::defragment_blocks_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::verify_draft_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::verify_draft_probabilistic_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::calculate_throughput_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::aggregate_stats_window_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::ema_update_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::calculate_memory_pressure_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::blocks_to_free_rust, m)?)?;

    // Phase 26: Multimodal & Structured Output Acceleration
    m.add_function(wrap_pyfunction!(multimodal::image_resize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::normalize_pixels_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::extract_video_frames_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::resample_audio_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::json_schema_to_regex_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::regex_match_prefix_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::compile_ebnf_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::grammar_next_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::consistent_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::select_worker_lb_rust, m)?)?;
    m.add_function(wrap_pyfunction!(multimodal::aggregate_worker_metrics_rust, m)?)?;

    // Phase 27: Attention, Quantization & LoRA Accelerations
    m.add_function(wrap_pyfunction!(quantlora::quantize_symmetric_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::quantize_asymmetric_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::dequantize_int4_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::pack_int4_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::compute_scales_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::lora_merge_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::attention_softmax_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::gqa_expand_kv_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::slot_mapping_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::batch_dequantize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::lora_forward_rust, m)?)?;
    
    // Phase 28: Request lifecycle, sampling, and detokenization
    m.add_function(wrap_pyfunction!(quantlora::request_status_transition_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::top_k_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::top_p_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::gumbel_sample_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::beam_score_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::check_stop_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::update_prefix_offset_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::compute_penalties_rust, m)?)?;

    // Phase 29: Execution Context, Batching & Async Streaming
    m.add_function(wrap_pyfunction!(quantlora::batch_descriptor_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::copy_with_indices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::pad_sequences_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::compute_dp_splits_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::pin_memory_copy_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::merge_batch_metadata_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::validate_batch_shapes_rust, m)?)?;

    // Phase 30: Engine Core, Output Processor & Incremental Detokenizer
    m.add_function(wrap_pyfunction!(quantlora::hash_block_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::check_stop_strings_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::detokenize_batch_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::merge_request_states_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::compute_prefix_match_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::validate_utf8_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::pack_outputs_rust, m)?)?;
    m.add_function(wrap_pyfunction!(quantlora::compute_cache_keys_rust, m)?)?;

    // Phase 32: UVA Buffer & GPU Transfer Accelerations
    m.add_function(wrap_pyfunction!(inference::uva_copy_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_write_indices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::coalesce_writes_rust, m)?)?;
    
    // Phase 32: Priority Scheduling Accelerations
    m.add_function(wrap_pyfunction!(inference::priority_heap_ops_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::token_budget_check_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::chunk_boundaries_rust, m)?)?;
    
    // Phase 32: Stream & Event Accelerations
    m.add_function(wrap_pyfunction!(inference::stream_sync_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::event_query_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::preemption_score_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::deadline_check_rust, m)?)?;

    // Phase 33: GPU Model Runner & Distributed Communication Accelerations
    m.add_function(wrap_pyfunction!(inference::prepare_positions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_idx_mapping_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::expand_idx_mapping_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::cudagraph_key_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::warmup_sizes_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::softmax_stable_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::persistent_gemm_tile_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::all_reduce_sum_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::rank_assignment_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::attention_dispatch_rust, m)?)?;

    // Phase 34: Disaggregated Inference & Advanced RoPE Accelerations
    m.add_function(wrap_pyfunction!(inference::rotary_embedding_kernel_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::mrope_section_indices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::dynamic_ntk_alpha_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::ngram_propose_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::eagle_tree_expand_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::kv_transfer_metadata_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::verify_draft_tokens_batch_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::block_table_lookup_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::triton_attention_dispatch_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::dcp_group_coordinate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::kv_connector_score_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::speculation_tree_parse_rust, m)?)?;
    
    // Phase 35: Async Execution & Advanced Caching
    m.add_function(wrap_pyfunction!(inference::block_pool_evict_lru_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::arc_cache_balance_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::prefix_tree_lookup_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::block_hash_compute_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::gpu_memory_snapshot_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::p2c_select_worker_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::step_counter_sync_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::wave_id_barrier_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::async_output_merge_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::dp_rank_coordinate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::kv_metrics_aggregate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::cache_hit_score_rust, m)?)?;

    // Phase 36: CUDA Graph & Compilation Accelerators
    m.add_function(wrap_pyfunction!(inference::batch_descriptor_key_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_ubatch_slices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::cudagraph_stats_compute_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::dispatch_decision_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_padded_buffer_size_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::analyze_shape_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::track_compile_event_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_optimal_graph_sizes_rust, m)?)?;

    // Phase 37: Weight Loading, KV Offload & Expert Load Balancing
    m.add_function(wrap_pyfunction!(inference::weight_hash_compute_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::validate_weight_shapes_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_shard_assignment_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::validate_shard_shapes_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_lru_eviction_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_arc_target_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_balanced_packing_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_expert_replication_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_load_imbalance_rust, m)?)?;

    // Phase 38: Advanced MoE Routing & SSM Acceleration
    m.add_function(wrap_pyfunction!(inference::moe_topk_route_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::moe_expert_choice_route_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::moe_aux_loss_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::ssm_discretize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::ssm_step_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::parallel_scan_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::causal_conv1d_update_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::silu_activation_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::mla_compress_kv_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::mla_head_mapping_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::soft_moe_route_rust, m)?)?;

    // Phase 39: Structured Output & Guided Decoding Acceleration
    m.add_function(wrap_pyfunction!(inference::regex_to_fsm_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::fill_token_bitmask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::validate_token_sequence_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::json_schema_fsm_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::apply_grammar_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_fill_bitmask_rust, m)?)?;
    
    // Phase 39: Speculative Decoding v2 - Tree-based Speculation
    m.add_function(wrap_pyfunction!(inference::build_speculation_tree_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::verify_speculation_tree_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::extract_accepted_path_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::speculation_stats_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::tensorizer_checksum_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::pack_tensor_metadata_rust, m)?)?;

    // Phase 40: Reasoning Parser Acceleration
    m.add_function(wrap_pyfunction!(inference::extract_thinking_blocks_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::parse_tool_calls_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::classify_token_context_rust, m)?)?;
    
    // Phase 40: Multimodal Cache Acceleration
    m.add_function(wrap_pyfunction!(inference::blake3_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::perceptual_hash_distance_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::lru_evict_candidates_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::arc_cache_priority_rust, m)?)?;
    
    // Phase 40: Pooling Engine Acceleration
    m.add_function(wrap_pyfunction!(inference::mean_pool_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::cls_pool_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::last_token_pool_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::matryoshka_truncate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::attention_pool_rust, m)?)?;
    
    // Phase 40: Input Preprocessing Acceleration
    m.add_function(wrap_pyfunction!(inference::estimate_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::validate_chat_messages_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::linearize_chat_rust, m)?)?;
    
    // Phase 40: Advanced Sampling Acceleration
    m.add_function(wrap_pyfunction!(inference::apply_temperature_schedule_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::apply_bad_words_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::apply_whitelist_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::mirostat_sample_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::adaptive_top_k_rust, m)?)?;

    // Phase 41: Tokenizer Registry Acceleration
    m.add_function(wrap_pyfunction!(inference::bpe_encode_fast_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_estimate_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::tokenizer_cache_key_rust, m)?)?;
    
    // Phase 41: Model Registry Acceleration
    m.add_function(wrap_pyfunction!(inference::architecture_fingerprint_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::estimate_vram_bytes_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::detect_architecture_rust, m)?)?;
    
    // Phase 41: LoRA Acceleration
    m.add_function(wrap_pyfunction!(inference::lora_scaling_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::lora_delta_compute_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::lora_adapter_hash_rust, m)?)?;
    
    // Phase 41: Logprobs Acceleration
    m.add_function(wrap_pyfunction!(inference::log_softmax_stable_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::extract_top_k_logprobs_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_perplexity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_entropy_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_logprobs_rust, m)?)?;
    
    // Phase 41: Tool Parser Acceleration
    m.add_function(wrap_pyfunction!(inference::extract_json_positions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::detect_tool_format_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::parse_tool_arguments_rust, m)?)?;
    
    // Phase 41: Structured Output Acceleration
    m.add_function(wrap_pyfunction!(inference::validate_json_schema_fast_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::validate_partial_json_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::constraint_hash_rust, m)?)?;

    // Phase 42: Platform Abstraction Acceleration
    m.add_function(wrap_pyfunction!(inference::platform_fingerprint_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::check_capability_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::estimate_memory_footprint_rust, m)?)?;
    
    // Phase 42: OpenAI Responses API Acceleration
    m.add_function(wrap_pyfunction!(inference::parse_response_json_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::parse_sse_event_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::encode_sse_event_rust, m)?)?;
    
    // Phase 42: Chat Template Acceleration
    m.add_function(wrap_pyfunction!(inference::render_simple_template_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::detect_chat_template_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::find_placeholders_rust, m)?)?;
    
    // Phase 42: MCP Tool Server Acceleration
    m.add_function(wrap_pyfunction!(inference::parse_mcp_tool_call_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::validate_mcp_schema_rust, m)?)?;
    
    // Phase 42: Conversation Context Acceleration
    m.add_function(wrap_pyfunction!(inference::hash_conversation_context_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::fast_token_count_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::truncate_tokens_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::generate_cache_salt_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::aggregate_token_metrics_rust, m)?)?;

    // Phase 43: KV Cache Coordination Acceleration
    m.add_function(wrap_pyfunction!(inference::compute_block_hashes_batched_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::calculate_blocks_needed_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_block_eviction_order_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::find_prefix_match_rust, m)?)?;
    
    // Phase 43: Request Queue Acceleration
    m.add_function(wrap_pyfunction!(inference::sort_requests_by_priority_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_fair_schedule_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_deadline_priorities_rust, m)?)?;
    
    // Phase 43: Parallel Sampling Acceleration
    m.add_function(wrap_pyfunction!(inference::generate_sample_seeds_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::rank_completions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_diversity_penalty_rust, m)?)?;
    
    // Phase 43: Iteration Metrics Acceleration
    m.add_function(wrap_pyfunction!(inference::compute_percentiles_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::detect_anomalies_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::compute_cache_hit_rate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::analyze_trend_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::aggregate_iteration_stats_rust, m)?)?;

    // Phase 44: Advanced Sampling & Speculative Decoding v2
    m.add_function(wrap_pyfunction!(inference::rejection_sample_verify_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::apply_top_k_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::apply_top_p_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_topk_topp_sample_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_apply_penalties_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::advanced_ngram_propose_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::encoder_content_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::encoder_cache_lru_evict_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::kv_cache_metrics_aggregate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::apply_typical_sampling_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::apply_min_p_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::gumbel_noise_rust, m)?)?;

    // Phase 45: Prometheus Metrics & Executor Acceleration
    m.add_function(wrap_pyfunction!(inference::cache_observe_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::histogram_observe_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::sliding_window_hit_rate_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::counter_increment_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::gauge_update_rust, m)?)?;
    
    // Phase 45: LoRA Stats Acceleration
    m.add_function(wrap_pyfunction!(inference::lora_stats_update_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::lora_latency_percentile_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::lora_adapter_lru_rust, m)?)?;
    
    // Phase 45: Caching Metrics Acceleration
    m.add_function(wrap_pyfunction!(inference::sliding_window_stats_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::eviction_breakdown_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::memory_pressure_rust, m)?)?;
    
    // Phase 45: Pooling Acceleration
    m.add_function(wrap_pyfunction!(inference::pool_sequences_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::pooling_cursor_advance_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::attention_weighted_pool_rust, m)?)?;
    
    // Phase 45: Logprobs Tensors Acceleration
    m.add_function(wrap_pyfunction!(inference::extract_top_k_batch_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::sparse_logprobs_store_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::logprobs_to_lists_rust, m)?)?;
    
    // Phase 45: Executor Task Acceleration
    m.add_function(wrap_pyfunction!(inference::task_priority_sort_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::worker_health_check_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::future_batch_complete_rust, m)?)?;
    
    // Phase 46: Structured Output Acceleration
    m.add_function(wrap_pyfunction!(inference::xgrammar_bitmask_fill_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::grammar_cache_key_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_update_indices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::bad_words_match_ngram_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::logit_bias_apply_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::min_p_threshold_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::structural_tag_parse_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::regex_dfa_transition_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::bad_words_trie_build_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::bad_words_prefix_check_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::batch_grammar_mask_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::template_extract_variables_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::json_schema_paths_rust, m)?)?;

    // Phase 47: Speculative Decoding V3 & KV Offload
    m.add_function(wrap_pyfunction!(inference::eagle_top_k_candidates_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::eagle_verify_accept_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::eagle_extrapolate_hidden_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::eagle_prepare_inputs_padded_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::ngram_find_match_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::ngram_fuzzy_match_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::prompt_lookup_propose_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::spec_decode_build_cu_indices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::spec_decode_build_logits_indices_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::spec_decode_verify_rejection_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::block_table_slot_mapping_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::arc_adaptation_delta_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::lru_eviction_priority_rust, m)?)?;
    m.add_function(wrap_pyfunction!(inference::tree_verification_paths_rust, m)?)?;

    Ok(())
}

