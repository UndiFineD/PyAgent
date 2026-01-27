use pyo3::prelude::*;

pub mod auction;
pub mod byzantine;
pub mod coder;
pub mod compliance;
pub mod consensus;
pub mod economy;
pub mod graph;
pub mod knowledge;
pub mod lesson;
pub mod localization;
pub mod memory;
pub mod pruning;
pub mod quality;
pub mod quantum;
pub mod redqueen;
pub mod research;
pub mod search;
pub mod stability;
pub mod synapse;
pub mod task;
pub mod tool;
pub mod web;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(pyo3::wrap_pyfunction!(auction::calculate_vcg_auction, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(auction::calculate_vcg_prices, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(auction::enforce_vram_quota, m)?)?;
    
    // Check if calculate_bid_priority_score is in economy or auction
    // Based on previous reads, it seems to be in economy.rs
    m.add_function(pyo3::wrap_pyfunction!(economy::calculate_bid_priority_score, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(byzantine::detect_deviating_hashes, m)?)?;
    // calculate_agreement_score is in byzantine OR consensus?
    // In byzantine.rs it is defined.
    // In consensus.rs it is favored.
    // I will check byzantine.rs export above... wait, I seemingly have duplicated it or it's in byzantine.
    // I will assume byzantine for now based on read_file output of byzantine.rs
    m.add_function(pyo3::wrap_pyfunction!(byzantine::calculate_agreement_score, m)?)?;
    
    m.add_class::<coder::CoderCore>()?;
    
    m.add_function(pyo3::wrap_pyfunction!(compliance::audit_content_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(compliance::aggregate_score_rust, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(consensus::calculate_consensus_winner, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(economy::calculate_gpu_surcharge, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(graph::extract_graph_entities_regex, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(graph::generate_mermaid_graph, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(graph::detect_cycles_rust, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(graph::filter_active_topology_relationships, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(knowledge::extract_python_symbols, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(knowledge::extract_markdown_backlinks, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(lesson::generate_failure_hash, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(localization::translate_key_terms, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(localization::detect_cultural_issues, m)?)?;

    m.add_function(pyo3::wrap_pyfunction!(memory::create_episode_struct, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(memory::calculate_new_utility, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(memory::filter_relevant_memories, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(pruning::calculate_decay_rust, m)?)?;
    
    m.add_class::<quality::CodeQualityCore>()?;
    
    m.add_function(pyo3::wrap_pyfunction!(quantum::calculate_superposition_weights, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(redqueen::evaluate_bypass, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(redqueen::filter_relevant_insights, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(research::execute_dcap_cycle, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(research::analyze_paper, m)?)?;
    m.add_function(pyo3::wrap_pyfunction!(research::draft_tool_code, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(search::aggregate_search_results, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(stability::detect_failed_agents_rust, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(synapse::calculate_synaptic_weight, m)?)?;
    
    m.add_function(pyo3::wrap_pyfunction!(task::generate_heuristic_plan, m)?)?;
    
    m.add_class::<tool::ToolDraftingCore>()?;
    
    m.add_class::<web::WebCore>()?;

    Ok(())
}
