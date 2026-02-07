use pyo3::prelude::*;
use std::collections::HashMap;

/// Create span context (TracingCore).
#[pyfunction]
pub fn create_span_context(trace_id: &str, span_id: &str) -> PyResult<HashMap<String, String>> {
    let mut context = HashMap::new();
    context.insert("trace_id".to_string(), trace_id.to_string());
    context.insert("span_id".to_string(), span_id.to_string());
    context.insert("version".to_string(), "OTel-1.1".to_string());
    Ok(context)
}

/// Calculate latency breakdown (TracingCore).
#[pyfunction]
pub fn calculate_latency_breakdown(total_time: f64, network_time: f64) -> PyResult<HashMap<String, f64>> {
    let thinking_time = total_time - network_time;
    let mut stats = HashMap::new();
    
    stats.insert("total_latency_ms".to_string(), total_time * 1000.0);
    stats.insert("network_latency_ms".to_string(), network_time * 1000.0);
    stats.insert("agent_thinking_ms".to_string(), thinking_time * 1000.0);
    
    let ratio = if total_time > 0.0 { thinking_time / total_time } else { 0.0 };
    stats.insert("think_ratio".to_string(), ratio);
    
    Ok(stats)
}
