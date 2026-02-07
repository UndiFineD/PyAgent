use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Calculate new utility score (MemoryCore).
#[pyfunction]
pub fn calculate_new_utility(old_score: f64, increment: f64) -> PyResult<f64> {
    Ok((old_score + increment).min(1.0).max(0.0))
}

/// Filter relevant memories by utility (MemoryCore).
#[pyfunction]
pub fn filter_relevant_memories(memories: Vec<Bound<'_, PyDict>>, min_utility: f64) -> PyResult<Vec<PyObject>> {
    let mut relevant = Vec::new();
    
    for mem in memories {
        // "utility_score" optional, default 0.0
        let score: f64 = if let Some(item) = mem.get_item("utility_score")? {
            item.extract().unwrap_or(0.0)
        } else {
            0.0
        };
        
        if score >= min_utility {
            relevant.push(mem.clone().into());
        }
    }
    
    Ok(relevant)
}

/// Create episode structure (MemoryCore).
/// Returns a PyDict directly for use in Python.
#[pyfunction]
pub fn create_episode_struct(
    py: Python<'_>,
    agent_name: &str,
    task: &str,
    outcome: &str,
    success: bool,
    baseline_utility: f64,
) -> PyResult<PyObject> {
    let dict = pyo3::types::PyDict::new(py);
    
    // Logic: if success +0.2 else -0.3
    let mut utility = baseline_utility;
    if success {
        utility += 0.2;
    } else {
        utility -= 0.3;
    }
    utility = utility.min(1.0).max(0.0);
    
    let now = chrono::Utc::now().to_rfc3339();
    
    dict.set_item("timestamp", now)?;
    dict.set_item("agent", agent_name)?;
    dict.set_item("task", task)?;
    dict.set_item("outcome", outcome)?;
    dict.set_item("success", success)?;
    dict.set_item("utility_score", utility)?;
    dict.set_item("metadata", pyo3::types::PyDict::new(py))?;
    
    Ok(dict.into())
}
