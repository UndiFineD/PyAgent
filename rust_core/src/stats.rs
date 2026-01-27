pub mod metrics;
pub mod stability;
pub mod tracing;
pub mod profiling;
pub mod general;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // metrics
    m.add_function(wrap_pyfunction!(metrics::calculate_token_cost, m)?)?;
    m.add_function(wrap_pyfunction!(metrics::select_best_model, m)?)?;
    m.add_function(wrap_pyfunction!(metrics::calculate_p95, m)?)?;
    // stability
    m.add_function(wrap_pyfunction!(stability::calculate_stability_score, m)?)?;
    m.add_function(wrap_pyfunction!(stability::is_in_stasis, m)?)?;
    m.add_function(wrap_pyfunction!(stability::get_healing_threshold, m)?)?;
    // tracing
    m.add_function(wrap_pyfunction!(tracing::create_span_context, m)?)?;
    m.add_function(wrap_pyfunction!(tracing::calculate_latency_breakdown, m)?)?;
    // profiling
    m.add_function(wrap_pyfunction!(profiling::calculate_optimization_priority, m)?)?;
    m.add_function(wrap_pyfunction!(profiling::identify_bottlenecks, m)?)?;
    // general
    m.add_function(wrap_pyfunction!(general::calculate_baseline, m)?)?;
    m.add_function(wrap_pyfunction!(general::check_regression, m)?)?;
    m.add_function(wrap_pyfunction!(general::score_efficiency, m)?)?;
    m.add_function(wrap_pyfunction!(general::calculate_priority_score, m)?)?;
    m.add_function(wrap_pyfunction!(general::calculate_token_estimate, m)?)?;
    m.add_function(wrap_pyfunction!(general::deduplicate_entries, m)?)?;
    m.add_function(wrap_pyfunction!(general::normalize_response, m)?)?;
    m.add_function(wrap_pyfunction!(general::assess_response_quality, m)?)?;
    Ok(())
}
