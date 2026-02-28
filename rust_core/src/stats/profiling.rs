use pyo3::prelude::*;

/// Calculate optimization priority (ProfilingCore).
#[pyfunction]
pub fn calculate_optimization_priority(total_time: f64, call_count: i64) -> PyResult<f64> {
    Ok(total_time * call_count as f64)
}

/// Identify bottlenecks (ProfilingCore).
/// Accepts a list of (function_name, total_time) tuples.
#[pyfunction]
pub fn identify_bottlenecks(stats: Vec<(String, f64)>, threshold_ms: f64) -> PyResult<Vec<String>> {
    let threshold_sec = threshold_ms / 1000.0;
    let mut bottlenecks = Vec::new();
    
    for (name, time) in stats {
        if time > threshold_sec {
            bottlenecks.push(name);
        }
    }
    
    Ok(bottlenecks)
}
