use pyo3::prelude::*;
use std::collections::{HashMap, HashSet};

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

// === MetricsCore Implementations ===

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

// === StabilityCore Implementations ===

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

// === TracingCore Implementations ===

/// Create span context (TracingCore).
#[pyfunction]
pub fn create_span_context(trace_id: &str, span_id: &str) -> PyResult<HashMap<String, String>> {
    let mut context = HashMap::new();
    context.insert("trace_id".to_string(), trace_id.to_string());
    context.insert("span_id".to_string(), span_id.to_string());
    context.insert("version".to_string(), "OTel-1.1".to_string());
    Ok(context)
}

/// Calculate latency breakdown (TracingCore).
#[pyfunction]
pub fn calculate_latency_breakdown(total_time: f64, network_time: f64) -> PyResult<HashMap<String, f64>> {
    let thinking_time = total_time - network_time;
    let mut stats = HashMap::new();
    
    stats.insert("total_latency_ms".to_string(), total_time * 1000.0);
    stats.insert("network_latency_ms".to_string(), network_time * 1000.0);
    stats.insert("agent_thinking_ms".to_string(), thinking_time * 1000.0);
    
    let ratio = if total_time > 0.0 { thinking_time / total_time } else { 0.0 };
    stats.insert("think_ratio".to_string(), ratio);
    
    Ok(stats)
}

// === ProfilingCore Implementations ===

/// Calculate optimization priority (ProfilingCore).
#[pyfunction]
pub fn calculate_optimization_priority(total_time: f64, call_count: i64) -> PyResult<f64> {
    Ok(total_time * call_count as f64)
}

/// Identify bottlenecks (ProfilingCore).
/// Accepts a list of (function_name, total_time) tuples.
#[pyfunction]
pub fn identify_bottlenecks(stats: Vec<(String, f64)>, threshold_ms: f64) -> PyResult<Vec<String>> {
    let threshold_sec = threshold_ms / 1000.0;
    let mut bottlenecks = Vec::new();
    
    for (name, time) in stats {
        if time > threshold_sec {
            bottlenecks.push(name);
        }
    }
    
    Ok(bottlenecks)
}

// === ModelFallbackCore Implementations ===

/// Get fallback chain (ModelFallbackCore).
#[pyfunction]
pub fn get_fallback_chain(primary: &str) -> PyResult<Vec<String>> {
    let chain = match primary {
        "gpt-4" => vec!["gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus"],
        "gpt-4-turbo" => vec!["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"],
        "claude-3-opus" => vec!["claude-3-sonnet", "gpt-4-turbo", "gemini-1.5-pro"],
        "gpt-3.5-turbo" => vec!["claude-3-haiku", "gemini-1.5-pro"],
        _ => vec![
            "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", 
            "claude-3-opus", "gemini-1.5-pro"
        ],
    };
    
    // Convert &str to String
    Ok(chain.into_iter().map(|s| s.to_string()).collect())
}

// === DeduplicationCore Implementations ===

/// Calculate Jaccard similarity.
/// Exposed for direct usage and testing.
#[pyfunction]
pub fn calculate_jaccard_similarity(s1: &str, s2: &str) -> PyResult<f64> {
    let set1: HashSet<String> = s1.to_lowercase().split_whitespace().map(|s| s.to_string()).collect();
    let set2: HashSet<String> = s2.to_lowercase().split_whitespace().map(|s| s.to_string()).collect();
    
    if set1.is_empty() || set2.is_empty() {
        return Ok(0.0);
    }
    
    let intersection_count = set1.intersection(&set2).count();
    let union_count = set1.len() + set2.len() - intersection_count;
    
    if union_count == 0 {
        return Ok(0.0);
    }
    
    Ok(intersection_count as f64 / union_count as f64)
}

/// Deduplicate based on Jaccard similarity.
/// Returns indices of items to keep.
/// This avoids returning complex dict objects, passing only strings.
#[pyfunction]
pub fn deduplicate_by_similarity(messages: Vec<String>, threshold: f64) -> PyResult<Vec<usize>> {
    let mut indices = Vec::new();
    let mut seen_sets: Vec<HashSet<String>> = Vec::new();

    for (i, msg) in messages.iter().enumerate() {
        let tokens: HashSet<String> = msg.to_lowercase()
            .split_whitespace()
            .map(|s| s.to_string())
            .collect();
            
        let mut is_duplicate = false;
        
        // Check against seen
        for seen in &seen_sets {
            // Calculate intersection on the fly
            let intersection = tokens.intersection(seen).count();
            let union = tokens.len() + seen.len() - intersection;
            
            let similarity = if union > 0 {
                intersection as f64 / union as f64
            } else {
                0.0
            };

            if similarity > threshold {
                is_duplicate = true;
                break;
            }
        }
        
        if !is_duplicate {
            seen_sets.push(tokens);
            indices.push(i);
        }
    }
    
    Ok(indices)
}

// === MetricsCore Implementations ===

/// Calculate statistical significance (ABTestCore).
/// Returns dict with p_value, t_statistic, effect_size.
#[pyfunction]
pub fn calculate_statistical_significance(
    py: Python<'_>,
    control_values: Vec<f64>,
    treatment_values: Vec<f64>
) -> PyResult<PyObject> {
    let dict = pyo3::types::PyDict::new(py);
    
    if control_values.is_empty() || treatment_values.is_empty() {
        dict.set_item("p_value", 1.0)?;
        dict.set_item("t_statistic", 0.0)?;
        dict.set_item("effect_size", 0.0)?;
        return Ok(dict.into());
    }

    let n_c = control_values.len() as f64;
    let n_t = treatment_values.len() as f64;

    let mean_c: f64 = control_values.iter().sum::<f64>() / n_c;
    let mean_t: f64 = treatment_values.iter().sum::<f64>() / n_t;

    let var_c: f64 = control_values.iter().map(|x| (x - mean_c).powi(2)).sum::<f64>() / n_c;
    let var_t: f64 = treatment_values.iter().map(|x| (x - mean_t).powi(2)).sum::<f64>() / n_t;

    // Pooled Standard Error
    let pooled_se = ((var_c / n_c) + (var_t / n_t)).sqrt();
    
    let t_stat = if pooled_se > 0.0 {
        (mean_t - mean_c) / pooled_se
    } else {
        0.0
    };

    let max_var = var_c.max(var_t);
    let effect_size = if max_var > 0.0 {
        (mean_t - mean_c) / max_var.sqrt()
    } else {
        0.0
    };

    // Simplified P-value lookup (Two-tailed approx)
    // t > 1.96 => p < 0.05
    let p_value = if t_stat.abs() > 1.96 { 0.05 } else { 0.95 };

    dict.set_item("p_value", p_value)?;
    dict.set_item("t_statistic", t_stat)?;
    dict.set_item("effect_size", effect_size)?;

    Ok(dict.into())
}

/// Calculate required sample size (ABTestCore).
#[pyfunction]
pub fn calculate_sample_size(effect_size: f64, alpha: Option<f64>, power: Option<f64>) -> PyResult<i64> {
    // defaults: alpha 0.05, power 0.8
    let _a = alpha.unwrap_or(0.05);
    let _p = power.unwrap_or(0.8);
    
    // z_alpha/2 (1.96) and z_beta (0.84)
    let z_alpha: f64 = 1.96;
    let z_beta: f64 = 0.84;
    
    if effect_size == 0.0 {
        return Ok(1_000_000);
    }
    
    let num = 2.0 * (z_alpha + z_beta).powi(2);
    let den = effect_size.powi(2);
    
    let n = (num / den).ceil() as i64;
    Ok(n)
}

/// Calculate average of values.
#[pyfunction]
pub fn calculate_avg(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    let sum: f64 = values.iter().sum();
    Ok(sum / values.len() as f64)
}

/// Calculate sum of values.
#[pyfunction]
pub fn calculate_sum(values: Vec<f64>) -> PyResult<f64> {
    Ok(values.iter().sum())
}

/// Calculate min of values.
#[pyfunction]
pub fn calculate_min(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    Ok(values.iter().fold(f64::INFINITY, |a, &b| a.min(b)))
}

/// Calculate max of values.
#[pyfunction]
pub fn calculate_max(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    Ok(values.iter().fold(f64::NEG_INFINITY, |a, &b| a.max(b)))
}

/// Calculate standard deviation.
#[pyfunction]
pub fn calculate_stddev(values: Vec<f64>) -> PyResult<f64> {
    let n = values.len() as f64;
    if n < 2.0 {
        return Ok(0.0);
    }
    let mean = values.iter().sum::<f64>() / n;
    let variance = values.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / (n - 1.0);
    Ok(variance.sqrt())
}

/// Calculate median (P50).
#[pyfunction]
pub fn calculate_median(values: Vec<f64>) -> PyResult<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    let mut sorted = values.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let mid = sorted.len() / 2;
    if sorted.len() % 2 == 0 {
        Ok((sorted[mid - 1] + sorted[mid]) / 2.0)
    } else {
        Ok(sorted[mid])
    }
}

/// Calculate rollups for time-series data (StatsRollupCalculator).
/// buckets: A list of (timestamp, value)
/// bucket_size: size of the bucket in seconds
#[pyfunction]
pub fn calculate_stats_rollup(points: Vec<(f64, f64)>, bucket_size: i64) -> PyResult<Vec<f64>> {
    if points.is_empty() || bucket_size <= 0 {
        return Ok(Vec::new());
    }

    use std::collections::BTreeMap;

    // Use BTreeMap to keep keys sorted automatically
    // Key: bucket index (timestamp // bucket_size)
    // Value: (sum, count)
    let mut buckets: BTreeMap<i64, (f64, usize)> = BTreeMap::new();

    for (ts, val) in points {
        let bucket_idx = (ts as i64) / bucket_size;
        let entry = buckets.entry(bucket_idx).or_insert((0.0, 0));
        entry.0 += val;
        entry.1 += 1;
    }

    let result: Vec<f64> = buckets.values()
        .map(|(sum, count)| sum / (*count as f64))
        .collect();

    Ok(result)
}

/// Estimates cyclomatic complexity from code text (EntropyCore).
/// Counts decision points: if, elif, for, while, and, or, except.
/// Complexity = 1 + decision_points.
#[pyfunction]
pub fn calculate_cyclomatic_complexity(code: &str) -> PyResult<i32> {
    use regex::Regex;
    // Basic regex that finds keywords ensuring they are whole words.
    let re = Regex::new(r"\b(if|elif|for|while|and|or|except)\b").unwrap();
    let matches = re.find_iter(code).count();
    Ok((1 + matches) as i32)
}

/// Checks if fine-tuning is needed based on quality history (ModelRegistryCore).
/// Returns true if the last `n` scores are all below `threshold`.
#[pyfunction]
pub fn check_finetuning_trigger(quality_history: Vec<f64>, threshold: f64, n_last: usize) -> PyResult<bool> {
    if quality_history.len() < n_last {
        return Ok(false);
    }
    
    // Check the last n scores
    let start_idx = quality_history.len() - n_last;
    for &score in &quality_history[start_idx..] {
        if score >= threshold {
            return Ok(false);
        }
    }
    
    Ok(true)
}

/// Calculate Pearson correlation coefficient (CorrelationAnalyzer).
#[pyfunction]
pub fn calculate_pearson_correlation(values_a: Vec<f64>, values_b: Vec<f64>) -> PyResult<f64> {
    let n = values_a.len().min(values_b.len());
    if n < 3 {
        return Ok(0.0);
    }
    
    let mean_a: f64 = values_a.iter().take(n).sum::<f64>() / n as f64;
    let mean_b: f64 = values_b.iter().take(n).sum::<f64>() / n as f64;
    
    let mut numerator = 0.0;
    let mut denom_a = 0.0;
    let mut denom_b = 0.0;
    
    for i in 0..n {
        let diff_a = values_a[i] - mean_a;
        let diff_b = values_b[i] - mean_b;
        numerator += diff_a * diff_b;
        denom_a += diff_a * diff_a;
        denom_b += diff_b * diff_b;
    }
    
    let denom = (denom_a.sqrt()) * (denom_b.sqrt());
    if denom == 0.0 {
        return Ok(0.0);
    }
    
    Ok(numerator / denom)
}

/// Predict future values using linear extrapolation (PredictionEngine).
#[pyfunction]
pub fn predict_linear(historical: Vec<f64>, periods: i32) -> PyResult<Vec<f64>> {
    if periods <= 0 || historical.is_empty() {
        return Ok(vec![]);
    }
    if historical.len() == 1 {
        return Ok(vec![historical[0]; periods as usize]);
    }
    
    let last = *historical.last().unwrap();
    let prev = historical[historical.len() - 2];
    let mut delta = last - prev;
    
    if delta == 0.0 && historical.len() > 2 {
        let window_size = historical.len().min(5);
        let window: Vec<f64> = historical.iter().rev().take(window_size).copied().collect();
        delta = (window[0] - window[window_size - 1]) / (window_size - 1) as f64;
    }
    
    let mut predictions = Vec::with_capacity(periods as usize);
    for i in 1..=periods {
        predictions.push(last + delta * i as f64);
    }
    
    Ok(predictions)
}

/// Calculate prediction with confidence intervals (PredictionEngine).
#[pyfunction]
pub fn predict_with_confidence_rust(historical: Vec<f64>, periods: i32) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    let predictions = predict_linear(historical.clone(), periods)?;
    
    if historical.is_empty() {
        let empty: Vec<f64> = vec![];
        return Ok((predictions.clone(), empty.clone(), empty));
    }
    
    let n = historical.len() as f64;
    let mean: f64 = historical.iter().sum::<f64>() / n;
    let var: f64 = historical.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / n;
    let std = var.sqrt();
    let margin = std.max(mean.abs() * 0.05);
    
    let lower: Vec<f64> = predictions.iter().map(|p| p - margin).collect();
    let upper: Vec<f64> = predictions.iter().map(|p| p + margin).collect();
    
    Ok((predictions, lower, upper))
}
