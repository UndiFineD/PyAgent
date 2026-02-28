use pyo3::prelude::*;

pub mod nlp;
pub mod matching;
pub mod search;
pub mod graph;
pub mod stats;
pub mod analysis;
pub mod knowledge;
pub mod processing;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // NLP
    m.add_function(wrap_pyfunction!(nlp::tokenize_and_index_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::tokenize_query_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::calculate_text_similarity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::find_similar_pairs_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::bulk_tokenize_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::word_frequencies_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::deduplicate_strings_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::cosine_similarity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::batch_cosine_similarity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(nlp::calculate_jaccard_set_rust, m)?)?;

    // Matching
    m.add_function(wrap_pyfunction!(matching::match_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(matching::bulk_match_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(matching::check_suppression_rust, m)?)?;
    m.add_function(wrap_pyfunction!(matching::scan_lines_multi_pattern_rust, m)?)?;
    m.add_function(wrap_pyfunction!(matching::batch_scan_files_rust, m)?)?;
    m.add_function(wrap_pyfunction!(matching::match_policies_rust, m)?)?;
    m.add_function(wrap_pyfunction!(matching::apply_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(matching::scan_compliance_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(matching::check_style_patterns_rust, m)?)?;

    // Search
    m.add_function(wrap_pyfunction!(search::search_content_scored_rust, m)?)?;
    m.add_function(wrap_pyfunction!(search::extract_versions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(search::search_with_tags_rust, m)?)?;
    m.add_function(wrap_pyfunction!(search::filter_memory_by_query_rust, m)?)?;
    m.add_function(wrap_pyfunction!(search::search_blocks_rust, m)?)?;

    // Analysis
    m.add_function(wrap_pyfunction!(analysis::analyze_code_quality_rust, m)?)?;
    m.add_function(wrap_pyfunction!(analysis::count_untyped_functions_rust, m)?)?;
    m.add_function(wrap_pyfunction!(analysis::find_duplicate_code_rust, m)?)?;
    m.add_function(wrap_pyfunction!(analysis::analyze_tech_debt_rust, m)?)?;
    m.add_function(wrap_pyfunction!(analysis::analyze_security_patterns_rust, m)?)?;
    m.add_function(wrap_pyfunction!(analysis::calculate_complexity_rust, m)?)?;
    m.add_function(wrap_pyfunction!(analysis::prepare_debt_records_rust, m)?)?;
    m.add_function(wrap_pyfunction!(analysis::validate_semver_rust, m)?)?;
    m.add_function(wrap_pyfunction!(analysis::analyze_failure_strategy_rust, m)?)?;

    // Graph
    m.add_function(wrap_pyfunction!(graph::calculate_coupling_rust, m)?)?;
    m.add_function(wrap_pyfunction!(graph::topological_sort_rust, m)?)?;
    m.add_function(wrap_pyfunction!(graph::build_graph_edges_rust, m)?)?;
    m.add_function(wrap_pyfunction!(graph::find_dependents_rust, m)?)?;

    // Stats
    m.add_function(wrap_pyfunction!(stats::linear_forecast_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::find_strong_correlations_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::aggregate_file_metrics_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_weighted_load_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::detect_failed_agents_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_variance_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::select_best_agent_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_sum_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_avg_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_min_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_max_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_median_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_p95_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_p99_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_stddev_rust, m)?)?;
    m.add_function(wrap_pyfunction!(stats::calculate_pearson_correlation_rust, m)?)?;

    // Knowledge
    m.add_function(wrap_pyfunction!(knowledge::normalize_and_hash_rust, m)?)?;
    m.add_function(wrap_pyfunction!(knowledge::fast_cache_key_rust, m)?)?;
    m.add_function(wrap_pyfunction!(knowledge::fast_prefix_key_rust, m)?)?;
    m.add_function(wrap_pyfunction!(knowledge::partition_to_shards_rust, m)?)?;
    m.add_function(wrap_pyfunction!(knowledge::calculate_shard_id_rust, m)?)?;
    m.add_function(wrap_pyfunction!(knowledge::merge_knowledge_rust, m)?)?;
    m.add_function(wrap_pyfunction!(knowledge::filter_stable_knowledge_rust, m)?)?;

    // Processing
    m.add_function(wrap_pyfunction!(processing::generate_unified_diff_rust, m)?)?;
    m.add_function(wrap_pyfunction!(processing::apply_template_rust, m)?)?;
    m.add_function(wrap_pyfunction!(processing::apply_simple_fixes_rust, m)?)?;
    m.add_function(wrap_pyfunction!(processing::bulk_replace_rust, m)?)?;
    m.add_function(wrap_pyfunction!(processing::bulk_replace_files_rust, m)?)?;
    m.add_function(wrap_pyfunction!(processing::scan_workspace_quality_rust, m)?)?;

    Ok(())
}
