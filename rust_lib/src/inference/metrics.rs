use pyo3::prelude::*;

// =============================================================================
// Phase 41: Logprobs Acceleration
// =============================================================================

/// Compute log softmax with numerical stability
#[pyfunction]
pub fn log_softmax_stable_rust(
    logits: Vec<f64>,
) -> Vec<f64> {
    let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let shifted: Vec<f64> = logits.iter().map(|l| l - max_logit).collect();
    let log_sum_exp = shifted.iter().map(|s| s.exp()).sum::<f64>().ln();
    
    shifted.iter().map(|s| s - log_sum_exp).collect()
}

/// Extract top-k logprobs with token IDs
/// Returns (top_k_ids, top_k_logprobs)
#[pyfunction]
pub fn extract_top_k_logprobs_rust(
    logprobs: Vec<f64>,
    k: usize,
) -> (Vec<usize>, Vec<f64>) {
    let mut indexed: Vec<(usize, f64)> = logprobs.into_iter().enumerate().collect();
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    indexed.truncate(k);
    
    let ids: Vec<usize> = indexed.iter().map(|(i, _)| *i).collect();
    let lps: Vec<f64> = indexed.iter().map(|(_, lp)| *lp).collect();
    
    (ids, lps)
}

/// Compute perplexity from logprobs
#[pyfunction]
pub fn compute_perplexity_rust(
    logprobs: Vec<f64>,
) -> f64 {
    if logprobs.is_empty() {
        return 0.0;
    }
    let mean_logprob: f64 = logprobs.iter().sum::<f64>() / logprobs.len() as f64;
    (-mean_logprob).exp()
}

/// Compute entropy from probability distribution
#[pyfunction]
pub fn compute_entropy_rust(
    probs: Vec<f64>,
) -> f64 {
    probs.iter()
        .filter(|&&p| p > 1e-10)
        .map(|&p| -p * p.ln())
        .sum()
}

/// Batch process logits to logprobs for multiple sequences
/// Returns flattened logprobs for selected tokens
#[pyfunction]
pub fn batch_logprobs_rust(
    batch_logits: Vec<Vec<f64>>,  // [batch, vocab]
    selected_ids: Vec<usize>,     // [batch]
) -> Vec<f64> {
    batch_logits.iter()
        .zip(selected_ids.iter())
        .map(|(logits, &token_id)| {
            let log_probs = {
                let max_logit = logits.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
                let shifted: Vec<f64> = logits.iter().map(|l| l - max_logit).collect();
                let log_sum_exp = shifted.iter().map(|s| s.exp()).sum::<f64>().ln();
                shifted.iter().map(|s| s - log_sum_exp).collect::<Vec<f64>>()
            };
            log_probs.get(token_id).copied().unwrap_or(f64::NEG_INFINITY)
        })
        .collect()
}

/// Cache observation with hit rate tracking
#[pyfunction]
pub fn cache_observe_rust(
    is_hit: bool,
    _bytes_accessed: i64,
    _latency_ns: i64,
    current_hits: i64,
    current_misses: i64,
) -> (i64, i64, f64) {
    let new_hits = current_hits + if is_hit { 1 } else { 0 };
    let new_misses = current_misses + if is_hit { 0 } else { 1 };
    let hit_rate = if new_hits + new_misses > 0 {
        new_hits as f64 / (new_hits + new_misses) as f64
    } else {
        0.0
    };
    (new_hits, new_misses, hit_rate)
}

/// Histogram observation with bucket assignment
#[pyfunction]
pub fn histogram_observe_rust(
    value: f64,
    buckets: Vec<f64>,
    current_counts: Vec<i64>,
    current_sum: f64,
) -> (Vec<i64>, f64, i64) {
    let mut new_counts = current_counts.clone();
    let new_sum = current_sum + value;
    let mut total_count = 0i64;
    
    for (i, &bucket) in buckets.iter().enumerate() {
        if value <= bucket {
            if i < new_counts.len() {
                new_counts[i] += 1;
            }
        }
        if i < new_counts.len() {
            total_count += new_counts[i];
        }
    }
    
    (new_counts, new_sum, total_count)
}

/// Sliding window hit rate calculation
#[pyfunction]
pub fn sliding_window_hit_rate_rust(
    events: Vec<(f64, bool, i64, i64)>,  // (timestamp, is_hit, bytes, latency)
    window_seconds: f64,
    current_time: f64,
) -> (i64, i64, f64, f64, f64) {
    let cutoff = current_time - window_seconds;
    
    let mut hits = 0i64;
    let mut misses = 0i64;
    let mut total_latency = 0i64;
    let mut total_bytes = 0i64;
    
    for (ts, is_hit, bytes, latency) in events {
        if ts > cutoff {
            if is_hit {
                hits += 1;
            } else {
                misses += 1;
            }
            total_latency += latency;
            total_bytes += bytes;
        }
    }
    
    let hit_rate = if hits + misses > 0 {
        hits as f64 / (hits + misses) as f64
    } else {
        0.0
    };
    
    let avg_latency = if hits + misses > 0 {
        total_latency as f64 / (hits + misses) as f64
    } else {
        0.0
    };
    
    (hits, misses, hit_rate, avg_latency, total_bytes as f64)
}

/// Counter increment with thread-safe semantics simulation
#[pyfunction]
pub fn counter_increment_rust(
    current: i64,
    increment: i64,
) -> i64 {
    current + increment
}

/// Gauge update with min/max tracking
#[pyfunction]
pub fn gauge_update_rust(
    _current: f64,
    new_value: f64,
    min_seen: f64,
    max_seen: f64,
) -> (f64, f64, f64) {
    (new_value, min_seen.min(new_value), max_seen.max(new_value))
}

/// Extract top-k logprobs batch
#[pyfunction]
pub fn extract_top_k_batch_rust(
    logprobs: Vec<Vec<f64>>,
    k: usize,
) -> Vec<(Vec<f64>, Vec<usize>)> {
    logprobs.into_iter().map(|row| {
        let mut indexed: Vec<(usize, f64)> = row.iter().enumerate().map(|(i, &v)| (i, v)).collect();
        indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        indexed.truncate(k);
        
        let values: Vec<f64> = indexed.iter().map(|(_, v)| *v).collect();
        let indices: Vec<usize> = indexed.iter().map(|(i, _)| *i).collect();
        (values, indices)
    }).collect()
}

/// Sparse logprobs storage
#[pyfunction]
pub fn sparse_logprobs_store_rust(
    logprobs: Vec<f64>,
    k: usize,
) -> (Vec<f64>, Vec<usize>) {
    let mut indexed: Vec<(usize, f64)> = logprobs.iter()
        .enumerate()
        .filter(|(_, &v)| v > f64::NEG_INFINITY)
        .map(|(i, &v)| (i, v))
        .collect();
    
    indexed.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    indexed.truncate(k);
    
    let values: Vec<f64> = indexed.iter().map(|(_, v)| *v).collect();
    let indices: Vec<usize> = indexed.iter().map(|(i, _)| *i).collect();
    
    (values, indices)
}

/// Logprobs to lists conversion
#[pyfunction]
pub fn logprobs_to_lists_rust(
    logprobs: Vec<Vec<Vec<f64>>>,  // (batch, seq, top_k)
    token_ids: Vec<Vec<Vec<usize>>>,  // (batch, seq, top_k)
) -> Vec<Vec<Vec<(usize, f64)>>> {
    logprobs.into_iter()
        .zip(token_ids.into_iter())
        .map(|(seq_lp, seq_ids)| {
            seq_lp.into_iter()
                .zip(seq_ids.into_iter())
                .map(|(pos_lp, pos_ids)| {
                    pos_lp.into_iter()
                        .zip(pos_ids.into_iter())
                        .map(|(lp, id)| (id, lp))
                        .collect()
                })
                .collect()
        })
        .collect()
}

