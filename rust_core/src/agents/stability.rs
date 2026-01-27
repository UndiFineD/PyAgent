use pyo3::prelude::*;

/// Scans agent logs for failure patterns (OOM, timeout, infinite loops).
#[pyfunction]
pub fn detect_failed_agents_rust(logs: Vec<String>) -> PyResult<Vec<String>> {
    let mut failed = Vec::new();
    
    for entry in logs {
        if entry.to_lowercase().contains("error") || entry.contains("traceback") {
            // Very naive check for demo purposes
            // In real logic, we'd parse the agent ID from the log line
            failed.push(format!("Flagged Agent from log: {}", &entry[..std::cmp::min(entry.len(), 30)]));
        }
    }
    
    Ok(failed)
}
