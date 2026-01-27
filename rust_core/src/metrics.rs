// Copyright 2026 PyAgent Authors
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::collections::HashMap;

/// Aggregate thousands of metric points per second (Common/Metrics).
#[pyfunction]
pub fn aggregate_metrics_rust(metrics: HashMap<String, Vec<f64>>) -> HashMap<String, f64> {
    let mut results = HashMap::new();
    for (name, values) in metrics {
        if !values.is_empty() {
            let sum: f64 = values.iter().sum();
            results.insert(name, sum / values.len() as f64);
        }
    }
    results
}

/// Fast rolling average calculation for metrics (Common/Metrics).
#[pyfunction]
pub fn rolling_avg_rust(values: Vec<f64>, window: usize) -> Vec<f64> {
    if window == 0 || values.is_empty() {
        return values;
    }
    let mut result = Vec::with_capacity(values.len());
    for i in 0..values.len() {
        let start = if i >= window { i - window + 1 } else { 0 };
        let slice = &values[start..=i];
        let avg: f64 = slice.iter().sum::<f64>() / slice.len() as f64;
        result.push(avg);
    }
    result
}

/// Calculate percentiles (p50, p90, p95, p99) across massive telemetry streams (Common/Telemetry).
#[pyfunction]
pub fn calculate_percentiles_rust(mut values: Vec<f64>) -> HashMap<String, f64> {
    let mut results = HashMap::new();
    if values.is_empty() {
        return results;
    }
    
    // Sort for percentile calculation
    values.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let len = values.len();
    
    let p_indices = [
        ("p50", 0.50),
        ("p90", 0.90),
        ("p95", 0.95),
        ("p99", 0.99),
    ];
    
    for (name, p) in p_indices {
        let idx = ((p * (len - 1) as f64).round() as usize).min(len - 1);
        results.insert(name.to_string(), values[idx]);
    }
    
    results
}

/// Calculate rollups (avg, max, count) across massive telemetry streams (Common/Telemetry).
#[pyfunction]
pub fn calculate_rollups(
    points: Vec<(String, f64, f64)>, // (name, timestamp, value)
    target_name: &str,
    window_seconds: f64,
    now: f64,
) -> PyResult<HashMap<String, f64>> {
    let mut sum = 0.0;
    let mut max = f64::MIN;
    let mut count = 0;

    for (name, timestamp, value) in points {
        if name == target_name && (now - timestamp) < window_seconds {
            sum += value;
            if value > max {
                max = value;
            }
            count += 1;
        }
    }

    let mut result = HashMap::new();
    if count == 0 {
        result.insert("avg".to_string(), 0.0);
        result.insert("max".to_string(), 0.0);
        result.insert("count".to_string(), 0.0);
    } else {
        result.insert("avg".to_string(), sum / count as f64);
        result.insert("max".to_string(), max);
        result.insert("count".to_string(), count as f64);
    }
    Ok(result)
}

/// Calculate percentiles (p50, p90, p95, p99) across massive telemetry streams (Common/Telemetry).
#[pyfunction]
pub fn percentiles(values: Vec<f64>) -> PyResult<HashMap<String, f64>> {
    Ok(calculate_percentiles_rust(values))
}

/// Aggregate multiple metric records (Mapping Alias).
#[pyfunction]
pub fn aggregate_metrics(metrics: HashMap<String, Vec<f64>>) -> HashMap<String, f64> {
    aggregate_metrics_rust(metrics)
}

/// Rolling average (Mapping Alias).
#[pyfunction]
pub fn rolling_avg(values: Vec<f64>, window: usize) -> Vec<f64> {
    rolling_avg_rust(values, window)
}

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
/// Calculate Pearson correlation coefficient (Common/Stats).
#[pyfunction]
pub fn calculate_pearson_correlation(x: Vec<f64>, y: Vec<f64>) -> PyResult<f64> {
    if x.len() != y.len() || x.is_empty() {
        return Ok(0.0);
    }
    let n = x.len() as f64;
    let sum_x: f64 = x.iter().sum();
    let sum_y: f64 = y.iter().sum();
    let sum_x2: f64 = x.iter().map(|&v| v * v).sum();
    let sum_y2: f64 = y.iter().map(|&v| v * v).sum();
    let sum_xy: f64 = x.iter().zip(&y).map(|(&a, &b)| a * b).sum();

    let numerator = n * sum_xy - sum_x * sum_y;
    let denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)).sqrt();

    if denominator.abs() < 1e-10 {
        Ok(0.0)
    } else {
        Ok(numerator / denominator)
    }
}

/// Simple Linear Regression prediction (Common/Stats).
#[pyfunction]
pub fn predict_linear(x: Vec<f64>, steps: usize) -> PyResult<Vec<f64>> {
    if x.len() < 2 {
        if let Some(&last) = x.last() {
            return Ok(vec![last; steps]);
        }
        return Ok(vec![0.0; steps]);
    }
    let n = x.len() as f64;
    let indices: Vec<f64> = (0..x.len()).map(|i| i as f64).collect();
    
    let sum_x: f64 = indices.iter().sum();
    let sum_y: f64 = x.iter().sum();
    let sum_xy: f64 = indices.iter().zip(&x).map(|(i, val)| i * val).sum();
    let sum_x2: f64 = indices.iter().map(|i| i * i).sum();

    let denominator = n * sum_x2 - sum_x * sum_x;
    if denominator.abs() < 1e-10 {
        let last = *x.last().unwrap_or(&0.0);
        return Ok(vec![last; steps]);
    }

    let slope = (n * sum_xy - sum_x * sum_y) / denominator;
    let intercept = (sum_y - slope * sum_x) / n;

    let mut predictions = Vec::with_capacity(steps);
    for i in 0..steps {
        let next_x = (x.len() + i) as f64;
        predictions.push(slope * next_x + intercept);
    }
    Ok(predictions)
}

<<<<<<< HEAD
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(aggregate_metrics_rust, m)?)?;
    m.add_function(wrap_pyfunction!(rolling_avg_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_percentiles_rust, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_rollups, m)?)?;
    m.add_function(wrap_pyfunction!(percentiles, m)?)?;
    m.add_function(wrap_pyfunction!(aggregate_metrics, m)?)?;
    m.add_function(wrap_pyfunction!(rolling_avg, m)?)?;
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    m.add_function(wrap_pyfunction!(calculate_pearson_correlation, m)?)?;
    m.add_function(wrap_pyfunction!(predict_linear, m)?)?;
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    m.add_function(wrap_pyfunction!(calculate_pearson_correlation, m)?)?;
    m.add_function(wrap_pyfunction!(predict_linear, m)?)?;
>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)
    Ok(())
}
