use pyo3::prelude::*;

/// Calculate stability score (StabilityCore).
/// Unpacks FleetMetrics fields: avg_error_rate, latency_p95.
#[pyfunction]
pub fn calculate_stability_score(avg_error_rate: f64, latency_p95: f64, sae_anomalies: i32) -> PyResult<f64> {
    let mut score = 1.0;
    
    // Penalties
    score -= avg_error_rate * 5.0;
    score -= sae_anomalies as f64 * 0.05;
    
    // Latency penalty
    let latency_penalty = f64::max(0.0, (latency_p95 - 2000.0) / 10000.0);
    score -= latency_penalty;
    
    // Clamp between 0.0 and 1.0
    Ok(score.max(0.0).min(1.0))
}

/// Check if fleet is in stasis (StabilityCore).
/// Returns true if variance is very low (< 0.0001).
#[pyfunction]
pub fn is_in_stasis(score_history: Vec<f64>) -> PyResult<bool> {
    if score_history.len() < 10 {
        return Ok(false);
    }
    
    let n = score_history.len() as f64;
    let mean = score_history.iter().sum::<f64>() / n;
    
    let variance = score_history.iter()
        .map(|x| (x - mean).powi(2))
        .sum::<f64>() / n;
        
    Ok(variance < 0.0001)
}

/// Get healing threshold logic (StabilityCore).
#[pyfunction]
pub fn get_healing_threshold(stability_score: f64) -> PyResult<f64> {
    if stability_score < 0.3 {
        Ok(0.9) // Aggressive healing
    } else {
        Ok(0.5) // Normal healing
    }
}
