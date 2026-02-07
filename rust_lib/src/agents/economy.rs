use pyo3::prelude::*;

/// Calculate bid priority (EconomyCore).
#[pyfunction]
pub fn calculate_bid_priority_score(credits: f64, importance: f64, urgency: f64) -> PyResult<f64> {
    Ok((credits * importance) * (1.0 + urgency))
}

/// Calculate GPU surcharge (EconomyCore).
#[pyfunction]
pub fn calculate_gpu_surcharge(vram_needed_gb: f64, current_utilization: f64) -> PyResult<f64> {
    let base_surcharge = vram_needed_gb * 0.5;
    let congestion_multiplier = 1.0 + current_utilization.powi(2);
    Ok(base_surcharge * congestion_multiplier)
}
