use pyo3::prelude::*;

#[pyfunction]
pub fn calculate_superposition_weights(prompts: Vec<String>) -> PyResult<Vec<f64>> {
    if prompts.is_empty() {
        return Ok(Vec::new());
    }

    let mut scores = Vec::with_capacity(prompts.len());
    for p in prompts {
        let mut score = p.len() as f64 * 0.01;
        let p_lower = p.to_lowercase();
        if p_lower.contains("logic") {
            score += 0.5;
        }
        if p_lower.contains("efficiency") {
            score += 0.3;
        }
        scores.push(score);
    }

    let exp_scores: Vec<f64> = scores.iter().map(|s| s.exp()).collect();
    let total: f64 = exp_scores.iter().sum();
    Ok(exp_scores.iter().map(|s| s / total).collect())
}

#[pyfunction]
#[allow(dead_code)]
pub fn simulate_interference_pattern(weights: Vec<f64>) -> PyResult<f64> {
    if weights.is_empty() {
        return Ok(0.0);
    }

    let mut entropy = 0.0;
    for &w in &weights {
        if w > 0.0 {
            entropy -= w * w.log2();
        }
    }
    Ok(entropy)
}
