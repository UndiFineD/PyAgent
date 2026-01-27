use pyo3::prelude::*;
use std::collections::HashMap;

// =============================================================================
// Phase 43: Iteration Metrics Acceleration
// =============================================================================

/// Compute sliding window percentiles
#[pyfunction]
pub fn compute_percentiles_rust(
    values: Vec<f64>,
    percentiles: Vec<f64>,
) -> Vec<f64> {
    if values.is_empty() {
        return vec![0.0; percentiles.len()];
    }
    
    let mut sorted = values.clone();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    
    percentiles.iter()
        .map(|&p| {
            let p_clamped = p.clamp(0.0, 100.0);
            let k = (sorted.len() - 1) as f64 * (p_clamped / 100.0);
            let f = k.floor() as usize;
            let c = std::cmp::min(f + 1, sorted.len() - 1);
            
            sorted[f] + (k - f as f64) * (sorted[c] - sorted[f])
        })
        .collect()
}

/// Detect anomalies using z-score
#[pyfunction]
pub fn detect_anomalies_rust(
    values: Vec<f64>,
    z_threshold: f64,
) -> Vec<bool> {
    if values.len() < 2 {
        return vec![false; values.len()];
    }
    
    let mean: f64 = values.iter().sum::<f64>() / values.len() as f64;
    let variance: f64 = values.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / values.len() as f64;
    let std = variance.sqrt();
    
    if std < 1e-10 {
        return vec![false; values.len()];
    }
    
    values.iter()
        .map(|&x| ((x - mean) / std).abs() > z_threshold)
        .collect()
}

/// Compute cache hit rate from sliding window
#[pyfunction]
pub fn compute_cache_hit_rate_rust(
    window_queries: Vec<i64>,
    window_hits: Vec<i64>,
) -> f64 {
    let total_queries: i64 = window_queries.iter().sum();
    let total_hits: i64 = window_hits.iter().sum();
    
    if total_queries == 0 {
        0.0
    } else {
        total_hits as f64 / total_queries as f64
    }
}

/// Analyze trend using linear regression
#[pyfunction]
pub fn analyze_trend_rust(
    timestamps: Vec<f64>,
    values: Vec<f64>,
) -> (String, f64) {
    if timestamps.len() < 2 || timestamps.len() != values.len() {
        return ("stable".to_string(), 0.0);
    }
    
    let n = timestamps.len() as f64;
    let sum_x: f64 = timestamps.iter().sum();
    let sum_y: f64 = values.iter().sum();
    let sum_xy: f64 = timestamps.iter().zip(values.iter()).map(|(x, y)| x * y).sum();
    let sum_xx: f64 = timestamps.iter().map(|x| x * x).sum();
    
    let denom = n * sum_xx - sum_x * sum_x;
    if denom.abs() < 1e-10 {
        return ("stable".to_string(), 0.0);
    }
    
    let slope = (n * sum_xy - sum_x * sum_y) / denom;
    
    let threshold = 0.01;
    let direction = if slope > threshold {
        "increasing"
    } else if slope < -threshold {
        "decreasing"
    } else {
        "stable"
    };
    
    (direction.to_string(), slope)
}

/// Aggregate iteration statistics
#[pyfunction]
pub fn aggregate_iteration_stats_rust(
    token_counts: Vec<i64>,
    latencies: Vec<f64>,
) -> HashMap<String, f64> {
    let mut result = HashMap::new();
    
    if token_counts.is_empty() {
        result.insert("total_tokens".to_string(), 0.0);
        result.insert("mean_latency".to_string(), 0.0);
        result.insert("throughput".to_string(), 0.0);
        return result;
    }
    
    let total_tokens: i64 = token_counts.iter().sum();
    let total_latency: f64 = latencies.iter().sum();
    let mean_latency = if !latencies.is_empty() { total_latency / latencies.len() as f64 } else { 0.0 };
    let throughput = if total_latency > 0.0 { total_tokens as f64 / total_latency } else { 0.0 };
    
    result.insert("total_tokens".to_string(), total_tokens as f64);
    result.insert("mean_latency".to_string(), mean_latency);
    result.insert("throughput".to_string(), throughput);
    
    result
}

// =============================================================================
// Phase 43: Metric Aggregation
// =============================================================================

/// Compute token metrics aggregation
#[pyfunction]
pub fn aggregate_token_metrics_rust(
    metrics_list: Vec<HashMap<String, i64>>,
) -> HashMap<String, i64> {
    let mut result: HashMap<String, i64> = HashMap::new();
    
    let keys = ["input_tokens", "output_tokens", "cached_tokens", "tool_tokens", "reasoning_tokens"];
    
    for key in keys {
        let sum: i64 = metrics_list.iter()
            .filter_map(|m| m.get(key))
            .sum();
        result.insert(key.to_string(), sum);
    }
    
    let total = result.get("input_tokens").unwrap_or(&0) + result.get("output_tokens").unwrap_or(&0);
    result.insert("total_tokens".to_string(), total);
    
    result
}

/// Compute KV cache metrics aggregates
#[pyfunction]
pub fn kv_cache_metrics_aggregate_rust(
    lifetimes: Vec<f64>,
    idle_times: Vec<f64>,
    access_counts: Vec<i64>,
) -> HashMap<String, f64> {
    let mut result = HashMap::new();
    
    if lifetimes.is_empty() {
        return result;
    }
    
    let n = lifetimes.len() as f64;
    
    // Lifetime stats
    let mean_lifetime: f64 = lifetimes.iter().sum::<f64>() / n;
    let mut sorted_lifetimes = lifetimes.clone();
    sorted_lifetimes.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let p50_lifetime = sorted_lifetimes[(n as usize * 50) / 100];
    let p95_lifetime = sorted_lifetimes[(n as usize * 95 / 100).min(sorted_lifetimes.len() - 1)];
    let p99_lifetime = sorted_lifetimes[(n as usize * 99 / 100).min(sorted_lifetimes.len() - 1)];
    
    result.insert("mean_lifetime".to_string(), mean_lifetime);
    result.insert("p50_lifetime".to_string(), p50_lifetime);
    result.insert("p95_lifetime".to_string(), p95_lifetime);
    result.insert("p99_lifetime".to_string(), p99_lifetime);
    
    // Idle time stats
    if !idle_times.is_empty() {
        let mean_idle: f64 = idle_times.iter().sum::<f64>() / idle_times.len() as f64;
        result.insert("mean_idle".to_string(), mean_idle);
    }
    
    // Access count stats
    if !access_counts.is_empty() {
        let mean_access: f64 = access_counts.iter().sum::<i64>() as f64 / access_counts.len() as f64;
        let zero_access_rate: f64 = access_counts.iter().filter(|&&c| c == 0).count() as f64 / access_counts.len() as f64;
        result.insert("mean_access_count".to_string(), mean_access);
        result.insert("zero_access_rate".to_string(), zero_access_rate);
    }
    
    result
}

/// Sliding window statistics calculation
#[pyfunction]
pub fn sliding_window_stats_rust(
    events: Vec<(f64, bool, i64, i64)>,  // (timestamp, is_hit, bytes, latency_ns)
    window_seconds: f64,
    current_time: f64,
) -> HashMap<String, f64> {
    let cutoff = current_time - window_seconds;
    
    let mut hits = 0i64;
    let mut misses = 0i64;
    let mut latencies: Vec<i64> = Vec::new();
    let mut total_bytes = 0i64;
    let mut first_ts = current_time;
    let mut last_ts = cutoff;
    
    for (ts, is_hit, bytes, latency) in events {
        if ts > cutoff {
            if is_hit { hits += 1; } else { misses += 1; }
            latencies.push(latency);
            total_bytes += bytes;
            first_ts = first_ts.min(ts);
            last_ts = last_ts.max(ts);
        }
    }
    
    let mut result = HashMap::new();
    result.insert("hits".to_string(), hits as f64);
    result.insert("misses".to_string(), misses as f64);
    result.insert("hit_rate".to_string(), if hits + misses > 0 { hits as f64 / (hits + misses) as f64 } else { 0.0 });
    
    if !latencies.is_empty() {
        latencies.sort();
        let sum: i64 = latencies.iter().sum();
        result.insert("avg_latency_ns".to_string(), sum as f64 / latencies.len() as f64);
        result.insert("p50_latency_ns".to_string(), latencies[latencies.len() / 2] as f64);
        result.insert("p99_latency_ns".to_string(), latencies[(latencies.len() as f64 * 0.99) as usize] as f64);
    }
    
    let duration = last_ts - first_ts;
    result.insert("bytes_per_second".to_string(), if duration > 0.0 { total_bytes as f64 / duration } else { 0.0 });
    result.insert("window_duration".to_string(), duration);
    
    result
}

/// Eviction breakdown by reason
#[pyfunction]
pub fn eviction_breakdown_rust(
    evictions: Vec<(f64, i32, i64)>,  // (timestamp, reason_code, bytes_freed)
) -> HashMap<i32, (i64, i64)> {
    let mut breakdown: HashMap<i32, (i64, i64)> = HashMap::new();
    
    for (_, reason, bytes) in evictions {
        let entry = breakdown.entry(reason).or_insert((0, 0));
        entry.0 += 1;
        entry.1 += bytes;
    }
    
    breakdown
}

/// Memory pressure calculation
#[pyfunction]
pub fn memory_pressure_rust(
    current_bytes: i64,
    peak_bytes: i64,
    eviction_rate: f64,
) -> f64 {
    let utilization = if peak_bytes > 0 {
        current_bytes as f64 / peak_bytes as f64
    } else {
        0.0
    };
    
    let eviction_pressure = (eviction_rate / 100.0).min(1.0);
    
    (utilization * 0.7) + (eviction_pressure * 0.3)
}

