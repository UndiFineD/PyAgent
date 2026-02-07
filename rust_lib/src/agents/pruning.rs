use pyo3::prelude::*;

/// Calculate synaptic decay across agent graphs (PruningCore).
#[pyfunction]
pub fn calculate_decay_rust(weights: Vec<f64>, decay_factor: f64) -> Vec<f64> {
    // decay_factor = age_seconds / half_life
    // Formula: weight * exp(-ln(2) * decay_factor)
    let ln2 = 0.69314718056;
    let exponent = -ln2 * decay_factor;
    let factor = exponent.exp();
    
    weights.into_iter().map(|w| (w * factor).max(0.05)).collect()
}
