use pyo3::prelude::*;

/// Calculate token cost based on model pricing (MetricsCore).
/// Returns (total_cost, input_cost, output_cost).
#[pyfunction]
pub fn calculate_token_cost(input_tokens: i64, output_tokens: i64, model: &str) -> PyResult<(f64, f64, f64)> {
    let (input_price, output_price) = match model {
        "gpt-4" => (0.03, 0.06),
        "gpt-4-turbo" => (0.01, 0.03),
        "gpt-3.5-turbo" => (0.0005, 0.0015),
        "claude-3-opus" => (0.015, 0.075),
        "claude-3-sonnet" => (0.003, 0.015),
        "claude-3-haiku" => (0.00025, 0.00125),
        "gemini-1.5-pro" => (0.0035, 0.0105),
        "llama-2-70b" => (0.0008, 0.001),
        _ => (0.0005, 0.0015), // Default to gpt-3.5-turbo
    };

    let input_cost = (input_tokens as f64 * input_price) / 1_000_000.0;
    let output_cost = (output_tokens as f64 * output_price) / 1_000_000.0;
    let total_cost = input_cost + output_cost;

    Ok((total_cost, input_cost, output_cost))
}

/// Select best model logic (MetricsCore).
#[pyfunction]
pub fn select_best_model(max_cost: f64, req_speed: f64, req_quality: f64) -> PyResult<String> {
    struct ModelCaps<'a> {
        name: &'a str,
        speed: f64,
        quality: f64,
        cost: f64,
    }

    let models = vec![
        ModelCaps { name: "gpt-4", speed: 0.5, quality: 1.0, cost: 0.1 },
        ModelCaps { name: "gpt-4-turbo", speed: 0.7, quality: 0.95, cost: 0.3 },
        ModelCaps { name: "gpt-3.5-turbo", speed: 0.9, quality: 0.7, cost: 0.8 },
        ModelCaps { name: "claude-3-opus", speed: 0.6, quality: 0.98, cost: 0.15 },
        ModelCaps { name: "gemini-1.5-pro", speed: 0.8, quality: 0.85, cost: 0.4 },
    ];

    let mut best_model = "gpt-3.5-turbo";
    let mut best_score = -1.0;

    for m in models {
        if m.cost <= max_cost && m.speed >= req_speed && m.quality >= req_quality {
            // formula: (speed * 0.3) + (quality * 0.5) + ((1 - cost) * 0.2)
            let score = (m.speed * 0.3) + (m.quality * 0.5) + ((1.0 - m.cost) * 0.2);
            if score > best_score {
                best_score = score;
                best_model = m.name;
            }
        }
    }

    Ok(best_model.to_string())
}

/// Calculate 95th percentile (MetricsCore).
#[pyfunction]
pub fn calculate_p95(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    
    // Check for small list edge case in Python code (< 20 items -> max)
    if values.len() < 20 {
        // Return max
        let max_val = values.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b));
        return Ok(max_val);
    }

    let mut sorted_vals = values.clone();
    // sort_by for f64 handles NaNs via unwrap or partial_cmp, assuming clean input per constraints
    sorted_vals.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    
    let idx = (sorted_vals.len() as f64 * 0.95) as usize;
    // Bounds check
    let idx = if idx >= sorted_vals.len() { sorted_vals.len() - 1 } else { idx };
    
    Ok(sorted_vals[idx])
}
