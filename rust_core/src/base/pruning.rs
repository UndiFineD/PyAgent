use pyo3::prelude::*;

/// Calculate synaptic decay (PruningCore).
#[pyfunction]
pub fn calculate_decay(current_weight: f64, idle_time_sec: f64, half_life_sec: f64) -> PyResult<f64> {
    // ln(2) approx 0.69314718056
    let decay_constant = 0.69314718056 / half_life_sec;
    let new_weight = current_weight * (-decay_constant * idle_time_sec).exp();
    Ok(f64::max(new_weight, 0.05))
}

/// Check if in refractory period (PruningCore).
#[pyfunction]
pub fn is_in_refractory(current_time: f64, refractory_until: f64) -> PyResult<bool> {
    Ok(current_time < refractory_until)
}

/// Update weight on fire (PruningCore).
#[pyfunction]
pub fn update_weight_on_fire_rust(current_weight: f64, success: bool) -> PyResult<f64> {
    if success {
        Ok(f64::min(current_weight * 1.1, 1.0))
    } else {
        Ok(f64::max(current_weight * 0.8, 0.1))
    }
}

/// Should prune (PruningCore).
#[pyfunction]
pub fn should_prune(weight: f64, threshold: f64) -> PyResult<bool> {
    Ok(weight < threshold)
}
