use pyo3::prelude::*;
use std::collections::HashMap;

/// Verify fleet health.
#[pyfunction]
pub fn verify_fleet_health(agent_reports: HashMap<String, bool>) -> PyResult<HashMap<String, PyObject>> {
    let mut results = HashMap::new();
    let total_count = agent_reports.len();
    let healthy_count = agent_reports.values().filter(|&&v| v).count();
    
    let all_passed = if total_count > 0 {
        healthy_count == total_count
    } else {
        false
    };

    let failed_agents: Vec<String> = agent_reports.iter()
        .filter(|(_, &v)| !v)
        .map(|(k, _)| k.clone())
        .collect();

    Python::with_gil(|py| {
        results.insert("all_passed".to_string(), all_passed.into_pyobject(py).unwrap().as_any().clone().unbind());
        results.insert("healthy_count".to_string(), healthy_count.into_pyobject(py).unwrap().as_any().clone().unbind());
        results.insert("total_count".to_string(), total_count.into_pyobject(py).unwrap().as_any().clone().unbind());
        results.insert("failed_agents".to_string(), failed_agents.into_pyobject(py).unwrap().as_any().clone().unbind());
    });

    Ok(results)
}
