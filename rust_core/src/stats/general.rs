use pyo3::prelude::*;
use std::collections::HashMap;

/// Calculates mean latency from benchmark results (pure calculation).
#[pyfunction]
pub fn calculate_baseline(latencies: Vec<f64>) -> PyResult<f64> {
    if latencies.is_empty() {
        return Ok(0.0);
    }
    let sum: f64 = latencies.iter().sum();
    Ok(sum / latencies.len() as f64)
}

/// Checks for performance regression against baseline.
#[pyfunction]
pub fn check_regression(
    current_latency: f64,
    baseline: f64,
    threshold: f64,
) -> PyResult<HashMap<String, f64>> {
    let mut result = HashMap::new();

    if baseline <= 0.0 {
        result.insert("regression".to_string(), 0.0);
        result.insert("delta".to_string(), 0.0);
        return Ok(result);
    }

    let delta = (current_latency - baseline) / baseline;
    result.insert(
        "regression".to_string(),
        if delta > threshold { 1.0 } else { 0.0 },
    );
    result.insert("delta_percentage".to_string(), delta * 100.0);
    result.insert("limit".to_string(), threshold * 100.0);
    Ok(result)
}

/// Calculates efficiency score (latency per token).
#[pyfunction]
pub fn score_efficiency(latency_ms: f64, token_count: i32) -> PyResult<f64> {
    if token_count <= 0 {
        return Ok(0.0);
    }
    Ok(latency_ms / token_count as f64)
}

/// Calculate priority score combining priority level and urgency.
/// BaseAgentCore equivalent (pure calculation).
#[pyfunction]
pub fn calculate_priority_score(priority_base: f64, urgency: f64) -> PyResult<f64> {
    // Blend priority with urgency (70% priority, 30% urgency)
    Ok((priority_base * 0.7) + (urgency * 0.3))
}

/// Estimate token count from text (character-based approximation).
#[pyfunction]
pub fn calculate_token_estimate(text: &str, chars_per_token: f64) -> PyResult<i32> {
    let token_count = (text.len() as f64 / chars_per_token).ceil() as i32;
    Ok(token_count.max(1))
}

/// Deduplicate string entries while preserving order.
#[pyfunction]
pub fn deduplicate_entries(entries: Vec<String>) -> PyResult<Vec<String>> {
    let mut seen = std::collections::HashSet::new();
    let mut result = Vec::new();
    
    for entry in entries {
        if seen.insert(entry.clone()) {
            result.push(entry);
        }
    }
    
    Ok(result)
}

/// Normalize response text (strip, standardize line endings, collapse spaces).
#[pyfunction]
pub fn normalize_response(response: &str) -> PyResult<String> {
    // Strip whitespace
    let normalized = response.trim();
    
    // Normalize line endings
    let normalized = normalized.replace("\r\n", "\n");
    
    // Collapse multiple spaces
    let words: Vec<&str> = normalized.split_whitespace().collect();
    Ok(words.join(" "))
}

/// Assess response quality (Logic only).
/// Returns a score from 0.0 to 1.0.
#[pyfunction]
pub fn assess_response_quality(response: &str, metadata: Option<HashMap<String, bool>>) -> PyResult<f64> {
    let mut score: f64 = 0.5;
    
    if response.len() > 100 {
        score += 0.1;
    }
    
    let lower = response.to_lowercase();
    if !lower.contains("error") && !lower.contains("fail") {
        score += 0.1;
    }
    
    if let Some(m) = metadata {
        if *m.get("has_references").unwrap_or(&false) {
            score += 0.1;
        }
        if *m.get("is_complete").unwrap_or(&false) {
            score += 0.1;
        }
    }
    
    Ok(score.min(1.0))
}
