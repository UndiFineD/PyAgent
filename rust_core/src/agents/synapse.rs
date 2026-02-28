use pyo3::prelude::*;

/// Calculates the weight of a synapse based on historical interactions.
#[pyfunction]
pub fn calculate_synaptic_weight(history_len: usize, success_rate: f64) -> PyResult<f64> {
    let base_weight: f64 = 1.0;
    let history_bonus = (history_len as f64).ln().max(0.0) * 0.1;
    let success_bonus = success_rate * 0.5;
    
    Ok(base_weight + history_bonus + success_bonus)
}
