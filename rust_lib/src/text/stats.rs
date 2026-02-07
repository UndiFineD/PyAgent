use pyo3::prelude::*;

#[pyfunction]
pub fn linear_forecast_rust(
    values: Vec<f64>,
    steps_ahead: usize,
) -> PyResult<Vec<f64>> {
    let n = values.len();
    if n < 2 {
        return Ok(Vec::new());
    }
    
    let x: Vec<f64> = (0..n).map(|i| i as f64).collect();
    let y = values;
    
    let sum_x: f64 = x.iter().sum();
    let sum_y: f64 = y.iter().sum();
    let sum_xy: f64 = x.iter().zip(y.iter()).map(|(a, b)| a * b).sum();
    let sum_xx: f64 = x.iter().map(|a| a * a).sum();
    
    let n_f = n as f64;
    let slope = (n_f * sum_xy - sum_x * sum_y) / (n_f * sum_xx - sum_x * sum_x);
    let intercept = (sum_y - slope * sum_x) / n_f;
    
    let mut forecast = Vec::new();
    for i in 1..=steps_ahead {
        let next_x = (n + i - 1) as f64;
        forecast.push(slope * next_x + intercept);
    }
    
    Ok(forecast)
}

#[pyfunction]
pub fn find_strong_correlations_rust(
    data: std::collections::HashMap<String, Vec<f64>>,
    threshold: f64,
) -> PyResult<Vec<(String, String, f64)>> {
    let keys: Vec<String> = data.keys().cloned().collect();
    let n = keys.len();
    let mut correlations = Vec::new();
    
    for i in 0..n {
        for j in (i + 1)..n {
            let col_a = &data[&keys[i]];
            let col_b = &data[&keys[j]];
            
            if col_a.len() != col_b.len() || col_a.is_empty() {
                continue;
            }
            
            let n_f = col_a.len() as f64;
            let mean_a = col_a.iter().sum::<f64>() / n_f;
            let mean_b = col_b.iter().sum::<f64>() / n_f;
            
            let numerator: f64 = col_a.iter().zip(col_b.iter())
                .map(|(a, b)| (a - mean_a) * (b - mean_b))
                .sum();
                
            let denom_a: f64 = col_a.iter().map(|a| (a - mean_a).powi(2)).sum();
            let denom_b: f64 = col_b.iter().map(|b| (b - mean_b).powi(2)).sum();
            
            if denom_a > 0.0 && denom_b > 0.0 {
                let r = numerator / (denom_a.sqrt() * denom_b.sqrt());
                if r.abs() >= threshold {
                    correlations.push((keys[i].clone(), keys[j].clone(), r));
                }
            }
        }
    }
    
    Ok(correlations)
}

#[pyfunction]
pub fn aggregate_file_metrics_rust(
    metrics: Vec<std::collections::HashMap<String, f64>>,
) -> PyResult<std::collections::HashMap<String, f64>> {
    let mut aggregation: std::collections::HashMap<String, f64> = std::collections::HashMap::new();
    let count = metrics.len() as f64;
    
    if count == 0.0 {
        return Ok(aggregation);
    }
    
    for m in &metrics {
        for (k, v) in m {
            *aggregation.entry(k.clone()).or_default() += v;
        }
    }
    
    // Calculate averages (or sums? Standard aggregation usually implies sum for some, avg for others. 
    // Assuming simple sum for now based on name, otherwise would need schema)
    // Actually, name implies "file metrics" -> maybe lines of code, etc. SUM is safest default for counts.
    // If it was latency, AVG would be better. Let's assume SUM as it's safer for "aggregation".
    // Alternatively, if this was used for stats, it might return mean.
    // Let's stick to Sum for consistency with previous Python list comprehension styles usually seen.
    
    Ok(aggregation)
}

#[pyfunction]
pub fn calculate_weighted_load_rust(
    loads: Vec<f64>,
    weights: Vec<f64>,
) -> PyResult<f64> {
    if loads.len() != weights.len() {
        return Ok(0.0);
    }
    
    let weighted_sum: f64 = loads.iter().zip(weights.iter()).map(|(l, w)| l * w).sum();
    let total_weight: f64 = weights.iter().sum();
    
    if total_weight == 0.0 {
        Ok(0.0)
    } else {
        Ok(weighted_sum / total_weight)
    }
}

#[pyfunction]
pub fn detect_failed_agents_rust(
    success_rates: std::collections::HashMap<String, f64>,
    threshold: f64,
) -> PyResult<Vec<String>> {
    let mut failed = Vec::new();
    
    for (agent, rate) in success_rates {
        if rate < threshold {
            failed.push(agent);
        }
    }
    
    Ok(failed)
}

#[pyfunction]
pub fn calculate_variance_rust(values: Vec<f64>) -> PyResult<f64> {
    if values.len() < 2 {
        return Ok(0.0);
    }
    
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let variance = values.iter().map(|value| {
        let diff = mean - value;
        diff * diff
    }).sum::<f64>() / (values.len() - 1) as f64;
    
    Ok(variance)
}

#[pyfunction]
pub fn select_best_agent_rust(
    agents: Vec<String>,
    scores: std::collections::HashMap<String, f64>,
) -> PyResult<Option<String>> {
    let mut best_agent = None;
    let mut best_score = -1.0; // Assuming scores are >= 0
    
    for agent in agents {
        if let Some(&score) = scores.get(&agent) {
            if score > best_score {
                best_score = score;
                best_agent = Some(agent);
            }
        }
    }
    
    Ok(best_agent)
}

#[pyfunction]
pub fn calculate_sum_rust(data: Vec<f64>) -> PyResult<f64> {
    Ok(data.iter().sum())
}

#[pyfunction]
pub fn calculate_avg_rust(data: Vec<f64>) -> PyResult<f64> {
    if data.is_empty() {
        return Ok(0.0);
    }
    Ok(data.iter().sum::<f64>() / data.len() as f64)
}

#[pyfunction]
pub fn calculate_min_rust(data: Vec<f64>) -> PyResult<f64> {
    let mut min_val = f64::INFINITY;
    for v in data {
        if v < min_val {
            min_val = v;
        }
    }
    Ok(if min_val == f64::INFINITY { 0.0 } else { min_val })
}

#[pyfunction]
pub fn calculate_max_rust(data: Vec<f64>) -> PyResult<f64> {
    let mut max_val = f64::NEG_INFINITY;
    for v in data {
        if v > max_val {
            max_val = v;
        }
    }
    Ok(if max_val == f64::NEG_INFINITY { 0.0 } else { max_val })
}

#[pyfunction]
pub fn calculate_median_rust(mut data: Vec<f64>) -> PyResult<f64> {
    if data.is_empty() {
        return Ok(0.0);
    }
    data.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let mid = data.len() / 2;
    if data.len() % 2 == 0 {
        Ok((data[mid - 1] + data[mid]) / 2.0)
    } else {
        Ok(data[mid])
    }
}

#[pyfunction]
pub fn calculate_p95_rust(mut data: Vec<f64>) -> PyResult<f64> {
    if data.is_empty() {
        return Ok(0.0);
    }
    data.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let idx = (data.len() as f64 * 0.95).floor() as usize;
    let idx = idx.min(data.len() - 1);
    Ok(data[idx])
}

#[pyfunction]
pub fn calculate_p99_rust(mut data: Vec<f64>) -> PyResult<f64> {
    if data.is_empty() {
        return Ok(0.0);
    }
    data.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let idx = (data.len() as f64 * 0.99).floor() as usize;
    let idx = idx.min(data.len() - 1);
    Ok(data[idx])
}

#[pyfunction]
pub fn calculate_stddev_rust(data: Vec<f64>) -> PyResult<f64> {
    if data.len() < 2 {
        return Ok(0.0);
    }
    let mean = data.iter().sum::<f64>() / data.len() as f64;
    let variance = data.iter().map(|value| {
        let diff = mean - value;
        diff * diff
    }).sum::<f64>() / (data.len() - 1) as f64;
    Ok(variance.sqrt())
}

#[pyfunction]
pub fn calculate_pearson_correlation_rust(x: Vec<f64>, y: Vec<f64>) -> PyResult<f64> {
    if x.len() != y.len() || x.len() < 2 {
        return Ok(0.0);
    }
    
    let n = x.len() as f64;
    let mean_x = x.iter().sum::<f64>() / n;
    let mean_y = y.iter().sum::<f64>() / n;
    
    let numerator: f64 = x.iter().zip(y.iter())
        .map(|(a, b)| (a - mean_x) * (b - mean_y))
        .sum();
        
    let denom_x: f64 = x.iter().map(|a| (a - mean_x).powi(2)).sum();
    let denom_y: f64 = y.iter().map(|b| (b - mean_y).powi(2)).sum();
    
    if denom_x == 0.0 || denom_y == 0.0 {
        return Ok(0.0);
    }
    
    Ok(numerator / (denom_x.sqrt() * denom_y.sqrt()))
}
