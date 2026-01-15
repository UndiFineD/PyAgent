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

// Imports for wrapping
use agents::*;
use base::*;
use stats::*;
use utils::*;

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

    // Base
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

    // Stats
    m.add_function(wrap_pyfunction!(calculate_baseline, m)?)?;
    m.add_function(wrap_pyfunction!(check_regression, m)?)?;
    m.add_function(wrap_pyfunction!(score_efficiency, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_priority_score, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_token_estimate, m)?)?;
    m.add_function(wrap_pyfunction!(deduplicate_entries, m)?)?;
    m.add_function(wrap_pyfunction!(normalize_response, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_token_cost, m)?)?;
    m.add_function(wrap_pyfunction!(select_best_model, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_cyclomatic_complexity, m)?)?;
    m.add_function(wrap_pyfunction!(check_finetuning_trigger, m)?)?;
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
    m.add_class::<CoderCore>()?;
    m.add_class::<ToolDraftingCore>()?;
    m.add_class::<WebCore>()?;
    m.add_class::<CodeQualityCore>()?;
    Ok(())
}

